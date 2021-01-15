#include "ssmsprovider.h"
#include <QDebug>
#include <QSqlError>
#include <QSqlQuery>
#include <QSqlRecord>
#include <QSqlField>

void SSMSProvider::setSchema(const QString &schema)
{
    m_schema = schema;
}

QString SSMSProvider::getSchema() const
{
    return m_schema;
}

QList<QVariantMap> SSMSProvider::get()
{
    QSqlQuery query(m_db);

    if(!query.prepare(queryString)) return {};

    for (auto && key : whereConditions.keys()) {
        query.bindValue(":" + key, whereConditions[key]);
    }

    if (!query.exec()) {
        qDebug() << "Error: " << query.lastError()
                 << "Query: " << query.lastQuery();
        return {};
    }

    QVariantMap row;
    QList<QVariantMap> res;
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

IDatabaseProvider &SSMSProvider::where(const QPair<QString, QVariant> &col)
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

IDatabaseProvider &SSMSProvider::whereIn(const QString field, const QVariantList &values)
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

IDatabaseProvider &SSMSProvider::whereNotIn(const QString field, const QVariantList &values)
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

SSMSProvider::SSMSProvider(QString databaseName, QString hostName, QString username, QString password)
{
    m_db = QSqlDatabase::database("SSMS");
    if(!m_db.isValid()) {
        m_db = QSqlDatabase::addDatabase("QODBC", "SSMS");
    }

#ifdef WIN64
    m_db.setDatabaseName(QString("DRIVER={SQL Server Native Client 10.0};"
                                 "Server=%1;Database=%2;Integrated Security = true;"
                                 "uid=%3;pwd=%4")
                         .arg(hostName, databaseName, username, password));
    qDebug() << QString("DRIVER={SQL Server Native Client 10.0};"
                        "Server=%1;Database=%2;Integrated Security = true;"
                        "uid=%3;pwd=%4")
                .arg(hostName, databaseName, username, password);
#else
    //msqls.setDatabaseName("Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.6.so.1.1};Server=192.168.81.201;Database=ewarehouse;Integrated Security = true");
    m_db.setDatabaseName(QString("DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.6.so.1.1};"
                                 "SERVER=%1;DATABASE=%2;Integrated Security = true;"
                                 "uid=%3;pwd=%4")
                         .arg(hostName, databaseName, username, password));
#endif


    m_db.setUserName(username);
    m_db.setPassword(password);
    if (!m_db.open()) {
        qDebug() << QString("Ошибка подключения к базе данных: %1")
                    .arg(m_db.lastError().text());
    }
}

SSMSProvider &SSMSProvider::selectJoin(const QList<QString> &fieldNames, const QString &secondTable, IDatabaseProvider::JoinType type, QString foreignKey, QString referencedField)
{
    Q_ASSERT(cond == ConditionType::INITSTATE);
    queryString = "SELECT :fieldNames FROM :schema.:tableName :joinType JOIN :secondTable ON :tableName.:foreignKey=:secondTable.:referencedKey";
    queryString.replace(":schema", m_schema);
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

int SSMSProvider::getLastID()
{
    return 0;
}

QVariant SSMSProvider::getRow(int index)
{
    return QVariant();
}

QVariant SSMSProvider::getRowField(const QString &fieldName, const QVariant &fieldValue)
{
    return QVariant();
}

QVariant SSMSProvider::getRowField(const QString &fieldName, const QVariant &fieldValue, int index)
{
    return QVariant();
}

SSMSProvider &SSMSProvider::select(const QList<QString> &field)
{
    Q_ASSERT(cond == ConditionType::INITSTATE);
    queryString = "SELECT :columns FROM [:schema].[:tableName] ";
    queryString.replace(":columns", field.isEmpty() ? "*" : toColumnString(field));
    queryString.replace(":tableName", getTableName());
    queryString.replace(":schema", m_schema);
    return *this;
}

bool SSMSProvider::updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value)
{

    queryString = "UPDATE [:schema].[:tableName] SET :appropriations WHERE :fieldName = :fieldValue";
    queryString.replace(":tableName", getTableName());
    queryString.replace(":schema", m_schema);
    QStringList updateAppr;
    for (auto && it = data.begin(); it != data.end(); it++) {
        QString pattern = ":col = ::col";
        updateAppr << pattern.replace(":col", it.key());
    }

    queryString.replace(":appropriations", updateAppr.join(", "));
    queryString.replace(":fieldName", value.first);

    qDebug() << queryString;
    QSqlQuery query(m_db);
    query.prepare(queryString);

    for (auto && it = data.begin(); it != data.end(); it++) {
        query.bindValue(":" + it.key(), it.value());
    }

    query.bindValue(":fieldValue", value.second);
    qDebug() << "update row" << query.lastQuery();
    return query.exec();
}

bool SSMSProvider::updateInsert(const QVariantMap &insertConditions,
                                const QVariantMap &insert,
                                const QVariantMap &update,
                                const QVariantMap &whereUpdate) const
{

    QSqlQuery q(m_db);
    QString operatorIs = "IS";
    QString operatorEquels = "=";
    QString query = "IF NOT EXISTS(SELECT * FROM [:schemaName].[:tableName] WHERE :insertConditions) "
            "BEGIN "
                "INSERT INTO [:schemaName].[:tableName] (:columnList) "
                "VALUES(:valueList) "
            "END "
            "ELSE "
            "BEGIN "
                "UPDATE [:schemaName].[:tableName] "
                "SET :updateList "
                "WHERE :whereUpdate "
            "END";

    QString insertConditionsString = "";
    QString insertColumnListString = "";
    QString insertValueListString = "";
    QString updateListString = "";
    QString whereUpdateString = "";

    query.replace(":schemaName", m_schema);
    query.replace(":tableName", getTableName());

    for (auto it = insertConditions.cbegin(), end = insertConditions.cend(); it != end; ++it) {
        QString patern = "(:col :operator :valCol) AND";
        patern.replace(":col", it.key());
        patern.replace(":operator", it.value().isNull() ? operatorIs : operatorEquels);
        patern.replace(":valCol", it.value().isNull() ? "NULL" : ":IC" + it.key());
        insertConditionsString.append(patern);
    }
    insertConditionsString = insertConditionsString.left(insertConditionsString.lastIndexOf("AND"));

    for (const auto &col: insert.keys()) {
        QString patern1 = ":col, ";
        QString patern2 = ":valCol, ";
        patern1.replace(":col", col);
        patern2.replace(":valCol", ":I" + col);
        insertColumnListString.append(patern1);
        insertValueListString.append(patern2);
    }
    insertColumnListString = insertColumnListString.left(insertColumnListString.lastIndexOf(","));
    insertValueListString = insertValueListString.left(insertValueListString.lastIndexOf(","));

    for (const auto &col: update.keys()) {
        QString patern = ":col = :valCol, ";
        patern.replace(":col", col);
        patern.replace(":valCol", ":U" + col);
        updateListString.append(patern);
    }
    updateListString = updateListString.left(updateListString.lastIndexOf(","));

    for (auto it = whereUpdate.cbegin(), end = whereUpdate.cend(); it != end; ++it) {
        QString patern = "(:col :operator :valCol) AND ";
        patern.replace(":col", it.key());
        patern.replace(":operator", it.value().isNull() ? operatorIs : operatorEquels);
        patern.replace(":valCol", it.value().isNull() ? "NULL" : ":WU" + it.key());
        whereUpdateString.append(patern);
    }
    whereUpdateString = whereUpdateString.left(whereUpdateString.lastIndexOf("AND"));

    query.replace(":tableName", getTableName());
    query.replace(":insertConditions", insertConditionsString);
    query.replace(":columnList", insertColumnListString);
    query.replace(":valueList", insertValueListString);
    query.replace(":updateList", updateListString);
    query.replace(":whereUpdate", whereUpdateString);
    qDebug() << "query" << query;
    q.prepare(query);

    for (auto it = insertConditions.cbegin(), end = insertConditions.cend(); it != end; ++it)
        q.bindValue(":IC" + it.key(), it.value());

    for (auto it = insert.cbegin(), end = insert.cend(); it != end; ++it)
        q.bindValue(":I" + it.key(), it.value());

    for (auto it = update.cbegin(), end = update.cend(); it != end; ++it)
        q.bindValue(":U" + it.key(), it.value());

    for (auto it = whereUpdate.cbegin(), end = whereUpdate.cend(); it != end; ++it)
        q.bindValue(":WU" + it.key(), it.value());

    if (q.exec()) {
        qDebug() << "\nError: " << q.lastError()
                 << "\nQuery: " << q.lastQuery();
        return true;
    } else {
        qDebug() << "\nError: " << q.lastError()
                 << "\nQuery: " << q.lastQuery();
        return false;
    }
}

bool SSMSProvider::insertRow(const QMap<QString, QVariant> &values)
{
    QSqlQuery q(m_db);
    QString query = "INSERT INTO [:schema].[:tableName] (:columns) VALUES(:values);";
    QString columnsString = toColumnString(values.keys());
    QString valuesString = ":" + values.keys().join(", :");
    query.replace(":schema", m_schema);
    query.replace(":tableName", getTableName());
    query.replace(":columns", columnsString);
    query.replace(":values", valuesString);
    q.prepare(query);
    for (auto at = values.cbegin(), end = values.cend(); at != end; ++at)
        q.bindValue(":" + at.key(), at.value());

    if (q.exec()) {
        return q.lastInsertId().toInt();
    } else {
        qDebug() << "\nError: " << q.lastError()
                 << "\nQuery: " << q.lastQuery();
        return -1;
    }

}

QString SSMSProvider::toColumnString(QStringList colList) const
{
    for (auto it = colList.begin(), end = colList.end(); it != end; ++it) {
        QString pattern = "[:col]";
        *it = pattern.replace(":col", *it);
    }
    const auto res = colList.join(", ");
    return res;
}

