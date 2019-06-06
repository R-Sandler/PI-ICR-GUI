/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.8.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionLoad_New_Reference;
    QAction *actionLoad_New_Measurement;
    QWidget *centralWidget;
    QComboBox *refClusterSelect;
    QComboBox *measClusterSelect;
    QLineEdit *refPhi;
    QLineEdit *measPhi;
    QLabel *label;
    QLabel *label_2;
    QLineEdit *refRadius;
    QLineEdit *measRadius;
    QLabel *label_3;
    QLabel *label_4;
    QLineEdit *Theta;
    QLineEdit *N;
    QLineEdit *Frequency;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QWidget *horizontalLayoutWidget;
    QHBoxLayout *horizontalLayout;
    QWidget *horizontalLayoutWidget_2;
    QHBoxLayout *horizontalLayout_2;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(669, 554);
        actionLoad_New_Reference = new QAction(MainWindow);
        actionLoad_New_Reference->setObjectName(QStringLiteral("actionLoad_New_Reference"));
        actionLoad_New_Measurement = new QAction(MainWindow);
        actionLoad_New_Measurement->setObjectName(QStringLiteral("actionLoad_New_Measurement"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        refClusterSelect = new QComboBox(centralWidget);
        refClusterSelect->setObjectName(QStringLiteral("refClusterSelect"));
        refClusterSelect->setGeometry(QRect(20, 320, 301, 22));
        measClusterSelect = new QComboBox(centralWidget);
        measClusterSelect->setObjectName(QStringLiteral("measClusterSelect"));
        measClusterSelect->setGeometry(QRect(350, 320, 301, 22));
        refPhi = new QLineEdit(centralWidget);
        refPhi->setObjectName(QStringLiteral("refPhi"));
        refPhi->setGeometry(QRect(110, 350, 121, 20));
        measPhi = new QLineEdit(centralWidget);
        measPhi->setObjectName(QStringLiteral("measPhi"));
        measPhi->setGeometry(QRect(440, 350, 121, 20));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(26, 350, 71, 20));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(360, 350, 71, 20));
        refRadius = new QLineEdit(centralWidget);
        refRadius->setObjectName(QStringLiteral("refRadius"));
        refRadius->setGeometry(QRect(110, 380, 121, 20));
        measRadius = new QLineEdit(centralWidget);
        measRadius->setObjectName(QStringLiteral("measRadius"));
        measRadius->setGeometry(QRect(440, 380, 121, 20));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(26, 380, 71, 20));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(360, 380, 71, 20));
        Theta = new QLineEdit(centralWidget);
        Theta->setObjectName(QStringLiteral("Theta"));
        Theta->setGeometry(QRect(272, 410, 131, 20));
        N = new QLineEdit(centralWidget);
        N->setObjectName(QStringLiteral("N"));
        N->setGeometry(QRect(272, 440, 131, 20));
        Frequency = new QLineEdit(centralWidget);
        Frequency->setObjectName(QStringLiteral("Frequency"));
        Frequency->setGeometry(QRect(272, 470, 131, 20));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(200, 410, 71, 20));
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(200, 440, 71, 20));
        label_7 = new QLabel(centralWidget);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(200, 470, 71, 20));
        horizontalLayoutWidget = new QWidget(centralWidget);
        horizontalLayoutWidget->setObjectName(QStringLiteral("horizontalLayoutWidget"));
        horizontalLayoutWidget->setGeometry(QRect(10, 10, 311, 281));
        horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
        horizontalLayout->setSpacing(6);
        horizontalLayout->setContentsMargins(11, 11, 11, 11);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        horizontalLayoutWidget_2 = new QWidget(centralWidget);
        horizontalLayoutWidget_2->setObjectName(QStringLiteral("horizontalLayoutWidget_2"));
        horizontalLayoutWidget_2->setGeometry(QRect(350, 10, 301, 281));
        horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 669, 21));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menuFile->menuAction());
        menuFile->addAction(actionLoad_New_Reference);
        menuFile->addAction(actionLoad_New_Measurement);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", Q_NULLPTR));
        actionLoad_New_Reference->setText(QApplication::translate("MainWindow", "Load New Reference", Q_NULLPTR));
        actionLoad_New_Measurement->setText(QApplication::translate("MainWindow", "Load New Measurement", Q_NULLPTR));
        label->setText(QApplication::translate("MainWindow", "Angle", Q_NULLPTR));
        label_2->setText(QApplication::translate("MainWindow", "Angle", Q_NULLPTR));
        label_3->setText(QApplication::translate("MainWindow", "Radius", Q_NULLPTR));
        label_4->setText(QApplication::translate("MainWindow", "Radius", Q_NULLPTR));
        label_5->setText(QApplication::translate("MainWindow", "Theta", Q_NULLPTR));
        label_6->setText(QApplication::translate("MainWindow", "N", Q_NULLPTR));
        label_7->setText(QApplication::translate("MainWindow", "Frequency", Q_NULLPTR));
        menuFile->setTitle(QApplication::translate("MainWindow", "File", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
