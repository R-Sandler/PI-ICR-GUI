#ifndef CALIBRATEWINDOW_H
#define CALIBRATEWINDOW_H

#include <QDialog>

namespace Ui {
class CalibrateWindow;
}

class CalibrateWindow : public QDialog
{
    Q_OBJECT

public:
    explicit CalibrateWindow(QWidget *parent = 0);
    ~CalibrateWindow();

private:
    Ui::CalibrateWindow *ui;
};

#endif // CALIBRATEWINDOW_H
