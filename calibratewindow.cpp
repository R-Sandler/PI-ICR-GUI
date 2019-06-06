#include "calibratewindow.h"
#include "ui_calibratewindow.h"

CalibrateWindow::CalibrateWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::CalibrateWindow)
{
    ui->setupUi(this);
}

CalibrateWindow::~CalibrateWindow()
{
    delete ui;
}
