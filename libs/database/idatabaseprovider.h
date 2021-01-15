#ifndef IDATABASEPROVIDER_H
#define IDATABASEPROVIDER_H

#include <QString>
#include <QVariant>
#include <QVariantMap>
#include <database_global.h>


class DATABASE_EXPORT IDatabaseProvider
{
    QString m_tableName;
public:
    IDatabaseProvider(){}

    enum class JoinType {INNER, LEFT, RIGHT, FULL};
    enum class ConditionType {WHERE, SELECT, INITSTATE};

    void setTable(QString name) {m_tableName = name;}
    virtual QVariant getRow(int index) = 0;
    virtual QVariant getRowField(const QString & fieldName, const QVariant & fieldValue) = 0;
    virtual QVariant getRowField(const QString & fieldName, const QVariant & fieldValue, int index) = 0;
    virtual IDatabaseProvider & select(const QList<QString> &field = {}) = 0;
    virtual bool insertRow(const QMap<QString, QVariant> & values) = 0;
    virtual bool updateRow(const QVariantMap &data, const QPair<QString, QVariant> &value) = 0;
    virtual int getLastID() = 0;
    virtual IDatabaseProvider & selectJoin(const QList<QString> &fieldNames, const QString &secondTable, JoinType type, QString foreignKey, QString referencedField) = 0;

    virtual QList<QVariantMap> get() = 0;
    virtual IDatabaseProvider & where(const QPair<QString, QVariant> & col) = 0;
    virtual IDatabaseProvider & whereIn(const QString field, const QVariantList & values) = 0;
    virtual IDatabaseProvider & whereNotIn(const QString field, const QVariantList & values) = 0;

    virtual ~IDatabaseProvider(){};

    QString getTableName() const {return m_tableName;}

protected: // internal
};

#endif // IDATABASEPROVIDER_H


