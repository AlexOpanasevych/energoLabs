#ifndef MYSQLPROVIDER_H
#define MYSQLPROVIDER_H

#include "idatabaseprovider.h"

#include <QSqlDatabase>

class DATABASE_EXPORT MySQLProvider : public IDatabaseProvider
{
    QSqlDatabase m_database;
    QVariantMap whereConditions;
    QString queryString;
    ConditionType cond = ConditionType::INITSTATE;
    int lastInID = 0;
public:
    MySQLProvider(QString databaseName = "", QString hostName = "", QString username = "", QString password = "");

    int getLastID() override;
    QVariant getRow(int index) override;
    QVariant getRowField(const QString &fieldName, const QVariant &fieldValue) override;
    MySQLProvider & select(const QList<QString> &field = {}) override;
    QVariant getRowField(const QString &fieldName, const QVariant &fieldValue, int index) override;
    bool insertRow(const QMap<QString, QVariant> &values) override;
    bool updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value) override;
    MySQLProvider & selectJoin(const QList<QString> &fieldNames, const QString &secondTable, JoinType type, QString foreignKey, QString referencedField) override;
    QList<QVariantMap> get() override;
    MySQLProvider & where(const QPair<QString, QVariant> &col) override;
    MySQLProvider & whereIn(const QString field, const QVariantList &values) override;
    MySQLProvider & whereNotIn(const QString field, const QVariantList &values) override;

};

#endif // MYSQLPROVIDER_H
