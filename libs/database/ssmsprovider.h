#ifndef SSMSPROVIDER_H
#define SSMSPROVIDER_H

#include "idatabaseprovider.h"

#include <QSqlDatabase>

class DATABASE_EXPORT SSMSProvider : public IDatabaseProvider
{
    QSqlDatabase m_db;
    QString m_schema;
    QString queryString;
    QVariantMap conditions;
    QVariantMap whereConditions;
    ConditionType cond = ConditionType::INITSTATE;
    int lastInID = 0;
public:
    SSMSProvider(QString databaseName, QString hostName, QString username, QString password);
    SSMSProvider & selectJoin(const QList<QString> &fieldNames, const QString &secondTable, JoinType type, QString foreignKey, QString referencedField) override;
    int getLastID() override;
    QVariant getRow(int index) override;
    QVariant getRowField(const QString &fieldName, const QVariant &fieldValue) override;
    QVariant getRowField(const QString &fieldName, const QVariant &fieldValue, int index) override;
    SSMSProvider & select(const QList<QString> &field = {}) override;
    bool updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value) override;
    bool insertRow(const QMap<QString, QVariant> &values) override;

    bool updateInsert(const QVariantMap &insertConditions,
                      const QVariantMap &insert,
                      const QVariantMap &update,
                      const QVariantMap &whereUpdate) const;

    QString toColumnString(QStringList colList) const;

    void setSchema(const QString &schema);
    QString getSchema() const;

    QList<QVariantMap> get() override;
    IDatabaseProvider & where(const QPair<QString, QVariant> & col) override;
    IDatabaseProvider & whereIn(const QString field, const QVariantList & values) override;
    IDatabaseProvider & whereNotIn(const QString field, const QVariantList & values) override;
};

#endif // SSMSPROVIDER_H
