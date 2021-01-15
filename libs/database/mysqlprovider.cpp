#include "mysqlprovider.h"

#include <QSqlQuery>
#include <QSqlRecord>
#include <QDebug>
#include <QSqlError>
#include <QSqlDriver>
#include <QSqlField>

MySQLProvider::MySQLProvider(QString databaseName, QString hostName, QString username, QString password)
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL");
    db.setHostName(hostName);
    if(!databaseName.isEmpty()) db.setDatabaseName(databaseName);
    else db.setDatabaseName("NEW_DATABASE");
    db.setUserName(username);
    db.setPassword(password);
    if(!db.open()) {
        qDebug() << "server not found";
        exit(EXIT_FAILURE);
    };
}

int MySQLProvider::getLastID()
{
    QSqlQuery query;
    QString queryString = "SELECT * FROM :tableName";
    queryString.replace(":tableName", getTableName());
    query.prepare(queryString);
    if(!query.exec()) return -1;
    else return query.size();
}

QVariant MySQLProvider::getRow(int index)
{
    return QVariant();
}

QVariant MySQLProvider::getRowField(const QString &fieldName, const QVariant &fieldValue)
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT * FROM :tableName WHERE :fieldName = :fieldValue";
    queryString.replace(":tableName", getTableName());
    queryString.replace(":fieldName", fieldName);

    if(!query.prepare(queryString)) return false;

    query.bindValue(":fieldValue", fieldValue);

    //qDebug() << "select query" << query.lastQuery() << fieldValue;
    if(query.exec() && query.isSelect()) {
        query.next();
        qDebug() << query.size() << query.executedQuery() << query.lastError();
        QSqlRecord rec = query.record();
        int index = rec.indexOf(fieldName);
        return query.value(index);
    }
    return {};
}

MySQLProvider & MySQLProvider::select(const QList<QString> &field)
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT :fieldNames FROM :tableName";
    queryString.replace(":tableName", getTableName());
    if(!field.isEmpty()) {
        queryString.replace(":fieldNames", field.join(", "));
    }
    else {
        queryString.replace(":fieldNames", "*");
    }

//    if(!fieldValue.isNull()) {
//        queryString += " WHERE :fieldName = :fieldValue";
//        queryString.replace(":fieldName", field);
//    }

    if(!query.prepare(queryString)) return *this;
    query.exec();

//    if(!fieldValue.isNull()) {
//        query.bindValue(":fieldValue", fieldValue);
//    }


    QVariantMap row;
    QList<QVariantMap> res;
    while(query.next()) {
        for (int i = 0, end = query.record().count(); i < end; ++i) {
            row[query.record().field(i).name()] = query.record().value(i);
        }
        res.append(row);
    }

    return *this;
}

QVariant MySQLProvider::getRowField(const QString &fieldName, const QVariant &fieldValue, int index)
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT * FROM :tableName WHERE :fieldName = :fieldValue";
    queryString.replace(":tableName", getTableName());
    queryString.replace(":fieldName", fieldName);

    if(!query.prepare(queryString)) return false;

    query.bindValue(":fieldValue", fieldValue);

    //qDebug() << "select query" << query.lastQuery() << fieldValue;
    if(query.exec() && query.isSelect()) {
        query.next();
        qDebug() << query.size() << query.executedQuery() << query.lastError();

        return query.value(index);
    }
    return {};
}

bool MySQLProvider::insertRow(const QMap<QString, QVariant> &values)
{
    if(values.isEmpty()) return false;
    QString queryString = "INSERT INTO ";
    QString val;
    val += "VALUES (";
    queryString += getTableName();
    queryString += " (";
    QMapIterator<QString, QVariant> i(values);
    while(i.hasNext()) {
        i.next();
        queryString += i.key();

        val += "?";
        if(i.hasNext()){
            queryString += ",";
            val += ",";
        }
        else {
            queryString += ") ";
            val += ");";
        }
    }
//    for(const auto & param : values) {

//    }
    queryString += val;

    QSqlQuery query(m_database);

    query.prepare(queryString);

    i.toFront();

    while(i.hasNext()) {
        i.next();
        query.addBindValue(i.value());
    }
    if(!query.exec()){
        qDebug() << query.lastError();
        return false;
    }
    return true;

}

bool MySQLProvider::updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value)
{
    QString queryString = "UPDATE TABLE :tableName SET :appropriations WHERE :fieldName = :fieldValue";
    queryString.replace(":tableName", getTableName());
    QStringList updateAppr;
    for (auto && it = data.begin(); it != data.end(); it++) {
        QString pattern = ":col = ::col";
        updateAppr << pattern.replace(":col", it.key());
    }

    queryString.replace(":appropriations", updateAppr.join(", "));
    queryString.replace(":fieldName", value.first);

    qDebug() << queryString;
    QSqlQuery query(m_database);
    query.prepare(queryString);

    for (auto && it = data.begin(); it != data.end(); it++) {
        query.bindValue(":" + it.key(), it.value());
    }

    query.bindValue(":fieldValue", value.second);
    qDebug() << "update row" << query.lastQuery();
    return query.exec();

}

MySQLProvider & MySQLProvider::selectJoin(const QList<QString> &fieldNames, const QString &secondTable, JoinType type, QString foreignKey, QString referencedField)
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT :fieldNames FROM :tableName :joinType JOIN :secondTable ON :tableName.:foreignKey=:secondTable.:referencedKey";
    queryString.replace(":tableName", getTableName());
    queryString.replace(":fieldNames", fieldNames.join(","));

    switch(type) {
    case JoinType::INNER:
        queryString.replace(":joinType", "INNER");
        break;
    case JoinType::LEFT:
        queryString.replace(":joinType", "LEFT");
        break;
    case JoinType::RIGHT:
        queryString.replace(":joinType", "RIGHT");
        break;
    case JoinType::FULL:
        queryString.replace(":joinType", "FULL");
        break;
    }

    queryString.replace(":secondTable", secondTable);
    queryString.replace(":foreignKey", foreignKey);
    queryString.replace(":referencedField", referencedField);



    return *this;

}

QList<QVariantMap> MySQLProvider::get()
{
    QSqlQuery q(m_database);
    if(!q.prepare(queryString)) return {};

    for (auto && key : whereConditions.keys()) {
        q.bindValue(":" + key, whereConditions[key]);
    }



    QList<QVariantMap> result;
    QVariantMap row;
    while(q.next()) {
        for (int i = 0, end = q.record().count(); i < end; ++i) {
            row[q.record().field(i).name()] = q.record().value(i);
        }
        result.append(row);
    }

    cond = ConditionType::INITSTATE;
    whereConditions.clear();
    lastInID = 0;
    return result;
}

MySQLProvider &MySQLProvider::where(const QPair<QString, QVariant> &col)
{
    if(!col.first.isEmpty() && col.second.isValid()) {
//        switch (cond) {
//        case ConditionType::SELECT: {
        if(whereConditions.isEmpty()) {
            Q_ASSERT(cond == ConditionType::SELECT);
            queryString += " WHERE :col = ::col ";
        }
        else queryString += " AND :col = ::col ";
        queryString.replace(":col", col.first);
        whereConditions[col.first] = col.second;
        cond = ConditionType::WHERE;
//        }
//        default:
//            return *this;
//        }

    }
    return *this;
}

MySQLProvider &MySQLProvider::whereIn(const QString field, const QVariantList &values)
{
    if(!field.isEmpty() && !values.isEmpty()) {
        if(whereConditions.isEmpty()) {
            Q_ASSERT(cond == ConditionType::SELECT);
            queryString += " WHERE :field IN (:values) ";
        }else {
            queryString += " AND :field IN (:values) ";
        }
        QStringList inValues;
        for(int i = 0; i < values.size(); i++) {
            whereConditions["inValue" + QString::number(lastInID + i)] = values[i];
        }
        lastInID = values.size();
        queryString.replace(":field", field);
        cond = ConditionType::WHERE;
    }
    return *this;
}

MySQLProvider &MySQLProvider::whereNotIn(const QString field, const QVariantList &values)
{
    if(!field.isEmpty() && !values.isEmpty()) {
        if(whereConditions.isEmpty()) {
            Q_ASSERT(cond == ConditionType::SELECT);
            queryString += " WHERE NOT :field IN (:values) ";
        }else {
            queryString += " AND NOT :field IN (:values) ";
        }
        QStringList notInValues;
        for(int i = 0; i < values.size(); i++) {
            whereConditions["inValue" + QString::number(lastInID + i)] = values[i];
        }
        lastInID = values.size();
        queryString.replace(":field", field);
        cond = ConditionType::WHERE;
    }
    return *this;
}
