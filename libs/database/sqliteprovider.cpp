#include "sqliteprovider.h"
#include <QtSql/QSqlError>
#include <QDebug>
#include <QSqlField>
#include <QSqlRecord>
#include <QSqlDriver>
#include <QDir>
#include <QUrl>

SqliteProvider::SqliteProvider(QString databaseName)
{
    m_database = QSqlDatabase::database("lite");
    if(!m_database.isValid())
        m_database = QSqlDatabase::addDatabase("QSQLITE", "lite");
    #ifdef WIN64
    qDebug() << QDir(databaseName).absolutePath();
        m_database.setDatabaseName(QDir(databaseName).absolutePath());
    #else
        m_database.setDatabaseName(QUrl("QML.db").path());
    #endif
    //m_database.setDatabaseName("C:\\Users\\prog5\\Documents\\myprojects\\HydraulicPressSoftware\\software\\database\\pressState.db");
    if(!m_database.open()) {
        qDebug() << "not connected" << m_database.lastError() << m_database.databaseName();
    }else {
        qDebug() << "connected to" << m_database.databaseName();
    }
}

QVariant SqliteProvider::getRow(int index)
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT * FROM :tableName WHERE :fieldName = :fieldValue";
    query.prepare("SELECT * FROM " + getTableName() + "WHERE id = " + QString::number(index));
    if(query.exec()) {
        query.next();
        return query.value(index);
    }
    return {};
}

QVariant SqliteProvider::getRowField(const QString & fieldName, const QVariant & fieldValue)
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

QVariant SqliteProvider::getRowField(const QString &fieldName, const QVariant &fieldValue, int index)
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

SqliteProvider & SqliteProvider::select(const QList<QString> &field)
{
    Q_ASSERT(cond == ConditionType::INITSTATE);
    QSqlQuery query(m_database);
    queryString = "SELECT :fields FROM :tableName";
    queryString.replace(":tableName", getTableName());
    queryString.replace(":fields", !field.empty() ? field.join(", ") : "*");
    cond = ConditionType::SELECT;
    return *this;
}

bool SqliteProvider::insertRow(const QMap<QString, QVariant> & values)
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

        val += ":" + i.key();
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
    Q_ASSERT(query.driver()->hasFeature(QSqlDriver::NamedPlaceholders));
    query.prepare(queryString);

    i.toFront();

    while(i.hasNext()) {
        i.next();
        query.bindValue(":" + i.key(), i.value());
    }
    if(!query.exec()){
        qDebug() << query.lastError() << query.executedQuery();
        return false;
    }
    return true;

}

/*
 * QSqlQuery q(m_db);
    QString query = "INSERT INTO :tableName (:columns) VALUES(:values);";
    QString columnsString = toColumnString(data.keys());
    QString valuesString = ":" + data.keys().join(", :");

    query.replace(":tableName", tableName);
    query.replace(":columns", columnsString);
    query.replace(":values", valuesString);
    q.prepare(query);
    for (auto at = data.cbegin(), end = data.cend(); at != end; ++at)
        q.bindValue(":" + at.key(), at.value());

    if (q.exec()) {
        return true;
    } else {
        qDebug() << "\nError: " << q.lastError()
                 << "\nQuery: " << q.lastQuery();
        return false;
    }
*/

bool SqliteProvider::updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value)
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

int SqliteProvider::getLastID()
{
    QSqlQuery query(m_database);
    QString queryString = "SELECT * FROM :tableName";
    queryString.replace(":tableName", getTableName());
    query.prepare(queryString);
    if(!query.exec()) return -1;
    else {
        query.last();
        return query.at() + 1;
    }
}

SqliteProvider & SqliteProvider::selectJoin(const QList<QString> &fieldNames, const QString &secondTable, JoinType type, QString foreignKey, QString referencedField)
{
    Q_ASSERT(cond == ConditionType::INITSTATE);
    queryString = "SELECT :fieldNames FROM :tableName :joinType JOIN :secondTable ON :tableName.:foreignKey=:secondTable.:referencedKey";
//    queryString.replace(":schema", m_schema);
    queryString.replace(":tableName", getTableName());

    bool firstTime = true;
    for (auto && field : fieldNames) {
        if(field.contains("MAX", Qt::CaseInsensitive)) {
            if(firstTime) {
                queryString += " GROUP BY ";
                firstTime = false;
            }
        }
        else if(!firstTime) {
            if(field != fieldNames.back())
                queryString += field + ", ";
            else queryString += field;
        }
    }

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
    queryString.replace(":referencedKey", referencedField);

    cond = ConditionType::SELECT;

    return *this;
}

QList<QVariantMap> SqliteProvider::get()
{
    QSqlQuery query(m_database);

    if(!query.prepare(queryString)) return {};

    for (auto && key : whereConditions.keys()) {
        query.bindValue(":" + key, whereConditions[key]);
    }

    QVariantMap row;
    QList<QVariantMap> res;
    query.exec();
    while(query.next()) {
        for (int i = 0, end = query.record().count(); i < end; ++i) {
            row[query.record().field(i).name()] = query.record().value(i);
        }
        res.append(row);
    }

    cond = ConditionType::INITSTATE;
    whereConditions.clear();
    lastInID = 0;

    return res;
}

IDatabaseProvider &SqliteProvider::where(const QPair<QString, QVariant> &col)
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

IDatabaseProvider &SqliteProvider::whereIn(const QString field, const QVariantList &values)
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

IDatabaseProvider &SqliteProvider::whereNotIn(const QString field, const QVariantList &values)
{
    Q_ASSERT(cond == ConditionType::SELECT);
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

//QString getLastExecutedQuery(const QSqlQuery& query)
//{
//    QString sql = query.executedQuery();
//    const int nbBindValues = query.boundValues().size();

//    for(int i = 0, j = 0; j < nbBindValues; ++j)
//    {
//        i = sql.indexOf(QLatin1Char('?'), i);
//        if (i <= 0)
//        {
//            break;
//        }
//        const QVariant &var = query.boundValue(j);
//        QSqlField field(QLatin1String(""), var.type());
//        if (var.isNull())
//        {
//            field.clear();
//        }
//        else
//        {
//            field.setValue(var);
//        }
//        QString formatV = query.driver()->formatValue(field);
//        sql.replace(i, 1, formatV);
//        i += formatV.length();
//    }

//    return sql;
//}

