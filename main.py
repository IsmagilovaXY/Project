import cv2
import numpy as np
import cv2 as cv


def f(args):
    pass


class Filter:
    def __init__(self):
        # fn = 'D:\\Practice\\Mscheme3.jpg'  # имя файла, который будем анализировать
        # img = cv.imread(fn)
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        ret, img = cap.read()
        rows = img.shape[0]
        self.minb = 0   # это заглушка нужно понять примерное значение при использовании непосредственно стенда
        self.ming = 0   # -//-
        self.minr = 0   # -//-
        self.maxb = 47   # -//-
        self.maxg = 213   # -//-
        self.maxr = 106   # -//-
        self.blur = 8   # -//-
        self.minDist = np.uint16(rows/8)   # -//-
        self.param1 = 30   # -//-
        self.param2 = 143   # -//-
        self.minRadius = 0   # -//-
        self.maxRadius = 82   # -//-
        self.mm_dev_pixels = 1   # -//-

    def filter_creation(self):
        # fn = 'D:\\Practice\\Mscheme3.jpg'  # имя файла, который будем анализировать
        # img = cv.imread(fn)
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        ret, img = cap.read()
        rows = img.shape[0]
        cv.namedWindow("result")
        cv.createTrackbar('minb', 'result', 0, 255, f)
        cv.createTrackbar('ming', 'result', 0, 255, f)
        cv.createTrackbar('minr', 'result', 0, 255, f)
        cv.createTrackbar('maxb', 'result', 255, 255, f)
        cv.createTrackbar('maxg', 'result', 255, 255, f)
        cv.createTrackbar('maxr', 'result', 255, 255, f)
        cv.createTrackbar("blur", "result", 0, 10, f)
        cv.namedWindow("HoughCircles")
        cv.createTrackbar('minDist', 'HoughCircles', np.uint16(rows/2), np.uint16(rows/2), f)
        cv.createTrackbar('param1', 'HoughCircles', 1, 1000, f)
        cv.createTrackbar('param2', 'HoughCircles', 1, 1000, f)
        cv.createTrackbar('minRadius', 'HoughCircles', 0, 1000, f)
        cv.createTrackbar('maxRadius', 'HoughCircles', 1, 1000, f)
        while True:
            # fn = 'D:\\Practice\\Mscheme3.jpg'  # имя файла, который будем анализировать
            # img = cv.imread(fn)
            ret, img = cap.read()
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            self.minb = cv.getTrackbarPos('minb', 'result')
            self.ming = cv.getTrackbarPos('minr', 'result')
            self.minr = cv.getTrackbarPos('ming', 'result')
            self.maxb = cv.getTrackbarPos('maxb', 'result')
            self.maxg = cv.getTrackbarPos('maxg', 'result')
            self.maxr = cv.getTrackbarPos('maxr', 'result')
            self.blur = cv.getTrackbarPos('blur', 'result')
            self.minDist = cv.getTrackbarPos('minDist', 'HoughCircles')
            self.param1 = cv.getTrackbarPos('param1', 'HoughCircles')
            self.param2 = cv.getTrackbarPos('param2', 'HoughCircles')
            self.minRadius = cv.getTrackbarPos('minRadius', 'HoughCircles')
            self.maxRadius = cv.getTrackbarPos('maxRadius', 'HoughCircles')
            img_bl = cv2.medianBlur(hsv, 1 + self.blur * 2)
            mask = cv.inRange(img_bl, (self.minb, self.ming, self.minr),
                              (self.maxb, self.maxg, self.maxr))
            cv.imshow('mask', mask)
            circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, self.minDist+1,
                                      param1=self.param1/10+0.1, param2=self.param2/10+0.1,
                                      minRadius=self.minRadius, maxRadius=self.maxRadius)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for c in circles[0, :]:
                    center = (c[0], c[1])
                    # circle center
                    cv.circle(img, center, 1, (0, 0, 255), 3)
                    # circle outline
                    radius = c[2]
                    cv.circle(img, center, radius, (0, 0, 255), 3)
                    if cv.waitKey(1) == ord("q"):
                        cv.destroyAllWindows()
                        return
            if cv.waitKey(1) == ord("q"):
                break
            cv.imshow('img', img)
        cv.destroyAllWindows()

    def calibration(self, mm_radius):
        # Работа с фото
        # fn = 'D:\\Practice\\Mscheme3.jpg'  # имя файла, который будем анализировать
        # img = cv.imread(fn)
        # Работа с камерой
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        radius_in_pixels_all = 0.0
        iterations = 0
        print('Калибровка может занять несколько минут')
        while iterations < 1000:
            # fn = 'D:\\Practice\\Mscheme3.jpg'  # имя файла, который будем анализировать
            # img = cv.imread(fn)
            ret, img = cap.read()
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            img_bl = cv2.medianBlur(hsv, 1 + self.blur * 2)
            mask = cv.inRange(img_bl, (self.minb, self.ming, self.minr),
                              (self.maxb, self.maxg, self.maxr))
            circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, self.minDist + 1,
                                      param1=self.param1 / 10 + 0.1, param2=self.param2 / 10 + 0.1,
                                      minRadius=self.minRadius, maxRadius=self.maxRadius)
            all_radii = 0
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for c in circles[0, :]:
                    center = (c[0], c[1])
                    # circle center
                    cv.circle(img, center, 1, (0, 0, 255), 3)
                    # circle outline
                    radius = c[2]
                    all_radii = all_radii + radius  # складываем все отмеченные кадре радиусы
                    cv.circle(img, center, radius, (0, 0, 255), 3)
            radius_in_pixels_all = radius_in_pixels_all + all_radii / len(circles)  # при условии что все контакты
            # одинакового радиуса складываются радиусы всех имеющихся на трансляции кругов,
            # а затем делится на их количество
            iterations = iterations + 1
        cv.destroyAllWindows()
        radius_in_pixels_all = radius_in_pixels_all / (iterations + 1)
        self.mm_dev_pixels = mm_radius / radius_in_pixels_all  # нахождение отношения мм к пикселям
        print("Калибровочное значение:")
        print(self.mm_dev_pixels)
        cap.release()


def detection(video_filter):
    # Работа с фото
    # fn = 'D:\\Practice\\wtf.jpg'  # имя файла, который будем анализировать
    # img = cv.imread(fn)

    # Работа с камерой
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    font = cv.FONT_HERSHEY_SIMPLEX
    while True:
        ret, img = cap.read()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        img_bl = cv2.medianBlur(hsv, 1 + video_filter.blur * 2)
        mask = cv.inRange(img_bl, (video_filter.minb, video_filter.ming, video_filter.minr),
                          (video_filter.maxb, video_filter.maxg, video_filter.maxr))
        circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, video_filter.minDist + 1,
                                  param1=video_filter.param1 / 10 + 0.1, param2=video_filter.param2 / 10 + 0.1,
                                  minRadius=video_filter.minRadius, maxRadius=video_filter.maxRadius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for c in circles[0, :]:
                center = (c[0], c[1])
                # circle center
                cv.circle(img, center, 1, (0, 0, 255), 2)
                text = \
                    (f"({round(c[0] * video_filter.mm_dev_pixels, 2)}, {round(c[1] * video_filter.mm_dev_pixels, 2)}, "
                     f"radius = {round(c[2] * video_filter.mm_dev_pixels, 2)})")
                cv.putText(img, text, (c[0] + 10, c[1] + 10),
                           font, 0.5, (0, 0, 255), 1)
                # circle outline
                radius = c[2]
                cv.circle(img, center, radius, (0, 0, 255), 2)

        # Рисуем оси
        cv.line(img, (0, 0), (img.shape[1], 0), (0, 255, 0), 2)  # Ось X
        cv.line(img, (0, 0), (0, img.shape[0]), (0, 0, 255), 2)  # Ось Y

        # Рисуем метки осей
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, "X", (img.shape[1] - 20, 20), font, 0.5, (0, 255, 0), 2)
        cv.putText(img, "Y", (20, img.shape[0] - 20), font, 0.5, (0, 0, 255), 2)

        # Рисуем точки с метками
        text_for_250_1 = f"(0, {round(250.0 * video_filter.mm_dev_pixels, 2)})"
        cv.circle(img, (0, 250), 5, (0, 0, 255), -1)  # Красная точка
        cv.putText(img, text_for_250_1, (0, 250 - 15), font, 0.5, (0, 0, 255), 1)

        text_for_250_2 = f"({round(250.0 * video_filter.mm_dev_pixels, 2)}, 0)"
        cv.circle(img, (250, 0), 5, (0, 255, 0), -1)  # Зеленая точка
        cv.putText(img, text_for_250_2, (250, 20), font, 0.5, (0, 255, 0), 1)

        text_for_500_1 = f"(0, {round(500.0 * video_filter.mm_dev_pixels, 2)})"
        cv.circle(img, (0, 500), 5, (0, 0, 255), -1)  # Красная точка
        cv.putText(img, text_for_500_1, (0, 500 - 15), font, 0.5, (0, 0, 255), 1)

        text_for_500_2 = f"({round(500.0 * video_filter.mm_dev_pixels, 2)}, 0)"
        cv.circle(img, (500, 0), 5, (0, 255, 0), -1)  # Зеленая точка
        cv.putText(img, text_for_500_2, (500, 20), font, 0.5, (0, 255, 0), 1)

        text_for_750_1 = f"(0, {round(750.0 * video_filter.mm_dev_pixels), 2})"
        cv.circle(img, (0, 750), 5, (0, 0, 255), -1)  # Красная точка
        cv.putText(img, text_for_750_1, (0, 750 - 15), font, 0.5, (0, 0, 255), 1)

        text_for_750_2 = f"({round(750.0 * video_filter.mm_dev_pixels, 2)}, 0)"
        cv.circle(img, (750, 0), 5, (0, 255, 0), -1)  # Зеленая точка
        cv.putText(img, text_for_750_2, (750, 20), font, 0.5, (0, 255, 0), 1)
        cv2.imshow('circles', img)
        if cv.waitKey(1) == ord("q"):
            break
    cv.destroyAllWindows()


print("Требуется ли настройка фильтра? Иначе будет использован фильтр по умолчанию. Если требуется, введите y")
answer1 = input()
my_filter = Filter()
if answer1 == 'y':
    my_filter.filter_creation()
print("Требуется ли дополнительная калибровка? Иначе будет использовано "
      "стандартное отношение мм/пикс. Если требуется, введите y")
answer2 = input()
if answer2 == 'y':
    print("Введите радиус контакта. Данное значение будет использовано как идеальное")
    ideal_radius = input()
    ideal_radius = float(ideal_radius)
    my_filter.calibration(ideal_radius)
detection(my_filter)
