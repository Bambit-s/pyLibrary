<?php
#Структурные 

use Dom\Text;

echo "__Adapter__\n";
// Adapter
## old class of paying (incompatible interface)
class LegacyPaymentSystem
{
    public function sendPayment(float $amountInDollars): string
    {
        return "Оплачено $amountInDollars USD через старую систему.";
    }
}

## new interface for paying
interface ModernPaymentInterface
{
    public function pay(float $amountInRubles): string;
}

## create adapter
class PaymentAdapter implements ModernPaymentInterface
{
    private LegacyPaymentSystem $legacyPayment;

    public function __construct(LegacyPaymentSystem $legacyPayment)
    {
        $this->legacyPayment = $legacyPayment;
    }
    public function pay(float $amountInRubles): string
    {
        $amountInDollars = $amountInRubles / 75;
        return $this->legacyPayment->sendPayment($amountInDollars);
    }
}

## using in client code
$legacyPayment = new LegacyPaymentSystem();
echo $legacyPayment->sendPayment(10) . "\n";

## adapter for new system
$adapter = new PaymentAdapter($legacyPayment);

## work with ModernPaymentInterface
function processPayment(ModernPaymentInterface $paymentSystem)
{
    echo $paymentSystem->pay(7500)  . "\n";
}

processPayment($adapter);

echo "__Bridge__\n";
// Bridge
## Мост разделяет абстракцию и реализацию намеренно, чтобы они могли развиваться независимо
interface Render
{
    public function renderCircle(float $radius): string;
    public function renderSquare(float $side): string;
}

class VectorRender implements Render
{
    public function renderCircle(float $radius): string
    {
        return "Отрисовка круга радиусом {$radius} в векторе.";
    }
    public function renderSquare(float $side): string
    {
        return "Отрисовка квадрата с со сторонами {$side} в векторе.";
    }
}

class RasterRender implements Render
{
    public function renderCircle(float $radius): string
    {
        return "Отрисовка круга радиусом {$radius} в растре.";
    }
    public function renderSquare(float $side): string
    {
        return "Отрисовка квадрата с со сторонами {$side} в растре.";
    }
}
## Ierarhy abstracts
abstract class Shape
{
    protected Render $render;

    public function __construct(Render $render)
    {
        $this->render = $render;
    }

    abstract public function draw(): string;
}

class Circle extends Shape
{
    private float $radius;

    public function __construct(Render $render, float $radius)
    {
        parent::__construct($render);
        $this->radius = $radius;
    }

    public function draw(): string
    {
        return $this->render->renderCircle($this->radius);
    }
}

class Square extends Shape
{
    private float $side;
    public function __construct(Render $render, float $side)
    {
        parent::__construct($render);
        $this->side = $side;
    }
    public function draw(): string
    {
        return $this->render->renderSquare($this->side);
    }
}
## create renderers
$vectorRender = new VectorRender();
$rasterRender = new RasterRender();
## create figures with different renderes
$circle = new Circle($vectorRender, 5);
$square = new Square($vectorRender, 10);

echo $circle->draw() . "\n";
echo $square->draw() . "\n";
$circle1 = new Circle($rasterRender, 5);
$square1 = new Square($rasterRender, 10);

echo $circle1->draw() . "\n";
echo $square1->draw() . "\n";

echo "__Composite__\n";
// Composite
# Композит позволяет сгруппировать множество объектов в древовидную структуру и работать с ней как с единым объектом.
# Организационная структура компании
## base component
interface Employee
{
    public function getName(): string;
    public function getSalary(): float;
    public function getRoles(): array;
    public function getSubordinates(): array;
    public function addSubordinate(Employee $employee): void;
}
## list(regular employer)
class Developer implements Employee
{
    private $name;
    private $salary;
    private $roles;

    public function __construct(string $name, float $salary, array $roles)
    {
        $this->name = $name;
        $this->salary = $salary;
        $this->roles = $roles;
    }
    public function getName(): string
    {
        return $this->name;
    }
    public function getSalary(): float
    {
        return $this->salary;
    }
    public function getRoles(): array
    {
        return $this->roles;
    }
    public function getSubordinates(): array
    {
        return [];
    }
    public function addSubordinate(Employee $employee): void
    {
        throw new Exception("Нельзя добавить подчиненного обычному сотруднику.");
    }
}

## composit manager
class Manager implements Employee
{
    private $name;
    private $salary;
    private $roles;
    private $subordinates = [];

    public function __construct(string $name, float $salary, array $roles)
    {
        $this->name = $name;
        $this->salary = $salary;
        $this->roles = $roles;
    }
    public function getName(): string
    {
        return $this->name;
    }
    public function getSalary(): float
    {
        return $this->salary;
    }
    public function getRoles(): array
    {
        return $this->roles;
    }
    public function getSubordinates(): array
    {
        return $this->subordinates;
    }
    public function addSubordinate(Employee $employee): void
    {
        $this->subordinates[] = $employee;
    }

    public function getTeamSalary(): float
    {
        $total = $this->getSalary();
        foreach ($this->subordinates as $subordinate) {
            $total += $subordinate instanceof Manager
                ? $subordinate->getTeamSalary()
                : $subordinate->getSalary();
        }
        return $total;
    }
}

## client code
$ceo = new Manager("Ivan Ivanovich", 500000, ['CEO']);
$cto = new Manager("Petr Petrovich", 300000, ['CTO']);
$devLead = new Manager("Sidorov Sidor", 200000, ['TeamLead']);
$dev1 = new Developer("Vladimir Vladimirovich", 150000, ['Backend']);
$dev2 = new Developer("Maksim Maksimovich", 120000, ['Frontend']);

$ceo->addSubordinate($cto);
$cto->addSubordinate($devLead);
$devLead->addSubordinate($dev1);
$devLead->addSubordinate($dev2);

echo "Общая зарплата команды: " . $ceo->getTeamSalary() . "\n";
echo "Подчиненные СТО:\n";
foreach ($cto->getSubordinates() as $subordinate) {
    echo "- " . $subordinate->getName() . "\n";
}
echo "__Decorator__:\n";
// Decorator 
# динамически добавлять новую функциональность объектам, не изменяя их исходный код. Работает как "обёртка" вокруг объекта.

## base interface and class
interface Notification
{
    public function send(): string;
}

class BasicNotificatiomd implements Notification
{
    public function send(): string
    {
        return "Базовое уведомление отправлено.";
    }
}

## base decorator
abstract class NotificationDecorator implements Notification
{
    protected Notification $notification;

    public function __construct(Notification $notification)
    {
        $this->notification = $notification;
    }
    abstract public function send(): string;
}

## special decorator
class EmailDecorator extends NotificationDecorator
{
    public function send(): string
    {
        return $this->notification->send() . "+ Email был отправлен.";
    }
}

class SmsDecorator extends NotificationDecorator
{
    public function send(): string
    {
        return $this->notification->send() . "+ Push был отправлен.";
    }
}

class PushDecorator extends NotificationDecorator
{
    public function send(): string
    {
        return $this->notification->send() . "+ Push был отправлен.";
    }
}

## client code
$notification = new BasicNotificatiomd();
echo $notification->send() . "\n";

$smsNotification = new SmsDecorator($notification);
echo $smsNotification->send() . "\n";

$smsEmailNotification = new EmailDecorator($smsNotification);
echo $smsEmailNotification->send() . "\n";

$smsEmailPushNotification = new PushDecorator($smsEmailNotification);
echo $smsEmailPushNotification->send() . "\n";

#Добавление логирования к HTTP-запросам#
#Форматирование текста (жирный + курсив + подчёркивание)#
#Дополнительные проверки в системе безопасности#

echo "__Facade__:\n";
// Facade
#скрывает сложность внутренних взаимодействий за единым упрощенным API.
class BluRayPlayer
{
    public function turnOn(): string
    {
        return "Плеер включен";
    }
    public function playMovie(string $movie): string
    {
        return "Воспроизведение фильма: {$movie}";
    }
}

class AudioSystem
{
    public function turnOn(): string
    {
        return "Аудиосистема включена";
    }
    public function setVolume(int $level): string
    {

        return "Громкость установлена на: {$level}";
    }
}

class Projector
{
    public function turnOn(): string
    {
        return "Проектор включен";
    }
    public function setInput(string $sourse): string
    {
        return "Источник проектора:{$sourse}";
    }
}

class Lights
{
    public function dim(int $percent): string
    {
        return "Освещение приглущено до {$percent}";
    }
}

## facade easy way to use cinema
class HomeTheaterFacde
{
    private BluRayPlayer $player;
    private AudioSystem $audio;
    private Projector $projector;
    private Lights $lights;

    public function __construct()
    {
        $this->player = new BluRayPlayer();
        $this->audio = new AudioSystem();
        $this->projector = new Projector();
        $this->lights = new Lights();
    }

    public function watchMovie(string $movie): string
    {
        $result = [];
        $result[] = $this->lights->dim(10);
        $result[] = $this->player->turnOn();
        $result[] = $this->audio->turnOn();
        $result[] = $this->audio->setVolume(60);
        $result[] = $this->projector->turnOn();
        $result[] = $this->projector->setInput("Blue-Ray");
        $result[] = $this->player->playMovie($movie);

        return implode("\n", $result);
    }

    public function endMovie(): string
    {
        return "Система выключается...\n";
    }
}

#cliente code
$theater = new HomeTheaterFacde();
echo $theater->watchMovie("Брат 2\n");
echo $theater->endMovie();

echo "__Flyweight__:\n";
// Flyweight
## который позволяет экономить память, разделяя общее состояние между множеством объектов, 
## вместо хранения одинаковых данных в каждом объекте.

# divided state
class FontSettings
{
    public function __construct(
        private string $font,
        private int $size,
        private string $color
    ) {}

    public function apply(string $char): string
    {
        return "Символ '$char' с настройками: {$this->font}, {$this->size}px, {$this->color}.'\n'";
    }
}

#fabrica Flyweight
class FontFactory
{
    private static array $fonts = [];

    public static function getFont(string $font, int $size, string $color): FontSettings
    {
        $key = "$font-$size-$color";
        if (!isset(self::$font[$key])) {
            self::$fonts[$key] = new FontSettings($font, $size, $color);
        }
        return self::$fonts[$key];
    }
}

#class with char Flyweight
class TextCharacter
{
    public function __construct(
        private string $char,
        private FontSettings $fontSettings,
    ) {}
    public function render(): string
    {
        return $this->fontSettings->apply($this->char);
    }
}

#client code
$chars = [];
$arialBlack = FontFactory::getFont('Arial', 12, 'black');
for ($i = 0; $i < 10; $i++) {
    $chars[] = new TextCharacter('A', $arialBlack);
}
foreach ($chars as $char_alone) {
    echo $char_alone->render();
}


echo "__Proxy__:\n";
// Proxy -> Заместитель
## подменяет реальный объект его суррогатом, контролируя доступ к нему. Прокси-объект имеет тот же интерфейс, что и реальный объект, что позволяет ему:
## Лениво инициализировать тяжелый объект
## Контролировать доступ
## Добавлять дополнительную логику

# Setvice interface
interface ImageLoaderInterface
{
    public function load(string $url): string;
}

# Real service(Heavy)
class RealImageLoader implements ImageLoaderInterface
{
    public function load(string $url): string
    {
        echo "Загрузка изображения с сервера..." . "\n";;
        sleep(2);
        return "Данные Изображения {$url}" . "\n";;
    }
}

# Proxy
class ImageLoaderProxy implements ImageLoaderInterface
{
    private ?RealImageLoader $realLoader = null;
    private array $cache = [];

    public function load(string $url): string
    {
        #lazy inicialization
        if ($this->realLoader === null) {
            $this->realLoader = new RealImageLoader();
        }
        #cache
        if (!isset($this->cache[$url])) {
            $this->cache[$url] = $this->realLoader->load($url);
        }

        return $this->cache[$url];
    }
}

# Client Code
function clientCode(ImageLoaderInterface $loader)
{
    echo $loader->load('image1.jpg') . "\n";
    echo $loader->load('image1.jpg') . "\n";
    echo $loader->load('image3.jpg') . "\n";
    echo $loader->load('image2.jpg') . "\n";
    echo $loader->load('image2.jpg') . "\n";
    echo $loader->load('image3.jpg') . "\n";
}

// echo "Без прокси" . "\n";
// clientCode(new RealImageLoader());
echo "С прокси" . "\n";
clientCode(new ImageLoaderProxy());
