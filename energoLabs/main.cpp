#include "dataprovider.h"

#include <QApplication>
#include <QProcess>
#include <QQmlApplicationEngine>
#include <QQmlContext>

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QApplication app(argc, argv);

    qmlRegisterType<QObject>("KLib", 1, 0, "");

    QProcess p;
    QObject::connect(&app, &QApplication::aboutToQuit, &p, &QProcess::kill);
    p.setProgram("python");
    p.setArguments(QStringList() << "../../energoLabs/script.py");
    p.start();
    QQmlApplicationEngine engine;
    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);
    auto provider = new DataProvider;
    engine.rootContext()->setContextProperty("dataProvider", provider);
    return app.exec();
}
