#ifndef DATAPROVIDER_H
#define DATAPROVIDER_H

#include <QObject>
//#include <kmacro.h>
#include <sqliteprovider.h>
#include <string>

class DataProvider : public QObject
{
    Q_OBJECT
//    K_QML_TYPE(DataProvider)
    SqliteProvider p;
public:
    explicit DataProvider(QObject *parent = nullptr);

public slots:
    QVariantList thirdGraphData(int dayFirst, int daySecond);

    QList<QVariantMap> get_electricity_dayOfWeek();
    QList<QVariantMap> get_electricity_electricalDevices();
    QList<QVariantMap> get_electricity_projectZone();
    QList<QVariantMap> get_electricity_switchType();
    QList<QVariantMap> get_electricity_tariff();
    QList<QVariantMap> get_electricity_tariffRange();
    QList<QVariantMap> get_electricity_tariffZone();
    QList<QVariantMap> get_electricity_userDevice();

    bool insert_electricity_dayOfWeek(QMap<QString, QVariant> & values);
    bool insert_electricity_electricalDevices(QMap<QString, QVariant> & values);
    bool insert_electricity_projectZone(QMap<QString, QVariant> & values);
    bool insert_electricity_switchType(QMap<QString, QVariant> & values);
    bool insert_electricity_tariff(QMap<QString, QVariant> & values);
    bool insert_electricity_tariffRange(QMap<QString, QVariant> & values);
    bool insert_electricity_tariffZone(QMap<QString, QVariant> & values);
    bool insert_electricity_userDevice(QMap<QString, QVariant> & values);

    QList<QVariantMap> getTableInfo(std::string nameTable);
    bool insertInfo(std::string nameTable, QMap<QString, QVariant> & values);

signals:



};

#endif // DATAPROVIDER_H
