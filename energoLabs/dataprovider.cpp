#include "dataprovider.h"

#include <QRandomGenerator>
#include <QVariantMap>
#include <QDebug>
#include <string>

DataProvider::DataProvider(QObject *parent) : QObject(parent), p("../../energoLabs/lab3.db")
{
    p.setTable("electrical_devices");
}

QVariantList DataProvider::thirdGraphData(int dayFirst, int daySecond)
{
    // here idk
    // p.select().where({"dayFirst", dayFirst}).where({"daySecond", daySecond}).get();
    qDebug() << "aadada";
    QVariantList result;
    for(int i = 0; i < qAbs(daySecond-dayFirst); i++) {
        QVariantMap map;
        map["x"] = QVariant(dayFirst+i);
        map["y"] = QVariant(QRandomGenerator::global()->bounded(0, 1000));
        result.append(map);
        qDebug() << map;
    }
    return result;
}

QList<QVariantMap> get_electricity_dayOfWeek()
{
    p.setTable("electricity_dayofweek");
    return p.get;
}

QList<QVariantMap> get_electricity_electricalDevices()
{
    p.setTable("electricity_electricaldevices");
    return p.get();
}

QList<QVariantMap> get_electricity_projectZone()
{
    p.setTable("electricity_projectzone");
    return p.get();
}

QList<QVariantMap> get_electricity_switchType()
{
    p.setTable("electricity_switchtype");
    return p.get();
}

QList<QVariantMap> get_electricity_tariff()
{
    p.setTable("electricity_tariff");
    return p.get();
}

QList<QVariantMap> get_electricity_tariffRange()
{
    p.setTable("electricity_tariffrange");
    return p.get();
}

QList<QVariantMap> get_electricity_tariffZone()
{
    p.setTable("electricity_tariffzone");
    return p.get();
}

QList<QVariantMap> get_electricity_userDevice()
{
    p.setTable("electricity_userdevice");
    return p.get();
}

bool insert_electricity_dayOfWeek(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_dayofweek");
    return p.insertRow(values);
}

bool insert_electricity_electricalDevices(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_electricaldevices");
    return p.insertRow(values);
}

bool insert_electricity_projectZone(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_projectzone");
    return p.insertRow(values);
}

bool insert_electricity_switchType(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_switchtype");
    return p.insertRow(values);
}

bool insert_electricity_tariff(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_tariff");
    return p.insertRow(values);
}

bool insert_electricity_tariffRange(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_tariffrange");
    return p.insertRow(values);
}

bool insert_electricity_tariffZone(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_tariffzone");
    return p.insertRow(values);
}

bool insert_electricity_userDevice(QMap<QString, QVariant> & values)
{
    p.setTable("electricity_userdevice");
    return p.insertRow(values);
}


QList<QVariantMap> DataProvider::getTableInfo(const std::string nameTable)
{
    p.setTable(nameTable);
    return p.get();
}

bool DataProvider::insertInfo(const std::string nameTable, const QMap<QString, QVariant> & values)
{
    p.setTable(nameTable);
    return p.insertRow(values);
}
