#include "widget.h"
#include "ui_widget.h"
#include <QFile>
#include <QTextStream>

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    this->setWindowTitle("Hello, Human!");
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_EnterButton_clicked()
{
    QString Greeting = "Hello, ";
    QString Username = ui->EnterName->text();
    if (Username == "") {
        ui->lineEdit->setText(" ");
    } else {
        ui->lineEdit->setText(Greeting+Username);
    }
}
