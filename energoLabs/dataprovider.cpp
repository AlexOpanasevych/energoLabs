#include "dataprovider.h"

#include <QRandomGenerator>
#include <QVariantMap>
#include <QDebug>

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
