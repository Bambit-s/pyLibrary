<?php
#Порождающие

// Фабрика
## определяет общий интерфейс для создания объектов, позволяя подклассам изменять тип создаваемых объектов.
interface Payment
{
    public function pay(float $amount): string;
}

class CreditCardPayment implements Payment
{
    public function pay(float $amount): string
    {
        return "Оплата $amount usd. через кредитную карту.";
    }
}
class PaypalCardPayment implements Payment
{
    public function pay(float $amount): string
    {
        return "Оплата $amount usd. через paypal карту.";
    }
}
class CryptoCardPayment implements Payment
{
    public function pay(float $amount): string
    {
        return "Оплата $amount usd. через crypto карту.";
    }
}

class PaymentFactory
{
    public static function createPayment(string $type): Payment
    {
        return match ($type) {
            'credit' => new CreditCardPayment(),
            'paypal' => new PaypalCardPayment(),
            'crypto' => new CryptoCardPayment(),
            default => throw new InvalidArgumentException("Неизвестный тип оплаты.")
        };
    }
}

$creditPayment = PaymentFactory::createPayment('credit');
$paypalPayment = PaymentFactory::createPayment('paypal');
$cryptoPayment = PaymentFactory::createPayment('crypto');
echo '___Фабрика___' . "\n";
echo $creditPayment->pay(5000) . "\n";
echo $paypalPayment->pay(2000) . "\n";
echo $cryptoPayment->pay(3000) . "\n";

// Абстрактная Фабрика
#позволяет создавать семейства связанных объектов, не привязываясь к конкретным классам.
#Она особенно полезена, когда система должна быть независимой от способа создания, компоновки и представления объектов, 
#а также когда нужно обеспечивать совместимость между создаваемыми объектами.

## интерфесы продуктов
interface Chair
{
    public function sit(): string;
}

interface Table
{
    public function eat(): string;
}
## создание абстрактной фабрики
interface FurnitureFactory
{
    public function createChair(): Chair;
    public function createTable(): Table;
}
## реализация конкретной фабрики
class ClassicFurnitureFactory implements FurnitureFactory
{
    public function createChair(): Chair
    {
        return new ClassicChair();
    }
    public function createTable(): Table
    {
        return new ClassicTable();
    }
}

class ModernFurnitureFactory implements FurnitureFactory
{
    public function createChair(): Chair
    {
        return new ModernChair();
    }

    public function createTable(): Table
    {
        return new ModernTable();
    }
}
## реализация конкретныъ продуктов
class ClassicChair implements Chair
{
    public function sit(): string
    {
        return "Я сижу на классическом стуле";
    }
}

class ClassicTable implements Table
{
    public function eat(): string
    {
        return "Я ем за классическим столом";
    }
}

class ModernChair implements Chair
{
    public function sit(): string
    {
        return "Я сижу на стуле модерн";
    }
}

class ModernTable implements Table
{
    public function eat(): string
    {
        return "Я ем за столом мрдерн";
    }
}
#Использование
function createFurniture(FurnitureFactory $factory)
{
    $chair = $factory->createChair();
    $table = $factory->createTable();

    echo $chair->sit() . "\n";
    echo $table->eat() . "\n";
}
echo '___Абстрактная Фабрика___' . "\n";
$classicFactory = new ClassicFurnitureFactory();
createFurniture($classicFactory);
$modernfactory = new ModernFurnitureFactory();
createFurniture($modernfactory);

// Строитель
## Паттерн Строитель (Builder) используется для пошагового создания сложных объектов, !отделяя конструирование от представления!. Особенно полезен, когда:
## Объект имеет много полей (например, конфигурация сервера, заказ в ресторане).
## Нужны разные варианты сборки (например, "минимум", "стандарт", "премиум").
## Процесс создания должен быть гибким (например, пропуск необязательных шагов).
class House
{
    public function __construct(
        public $name,
        public $number,
    ) {}
}

class HouseBuilder
{
    private string $name;
    private string $number;

    public function setName($name)
    {
        $this->name = $name;
        return $this;
    }

    public function setNumber($number)
    {
        $this->number = $number;
        return $this;
    }

    // Метод для создания итогового объекта House
    public function build()
    {
        // Создаем и возвращаем новый объект House с сохраненными значениями
        return new House(
            $this->name,
            $this->number,
        );
    }
}

# Использование строителя:
# 1. Создаем новый экземпляр HouseBuilder
# 2. Устанавливаем название "Casa" через setName()
# 3. Устанавливаем номер "7" через setNumber()
# 4. Вызываем build() для создания итогового объекта House
$house = (new HouseBuilder())->setName("Casa")->setNumber('7')->build();
echo '___Строитель___';
# Выводим информацию о созданном объекте House
var_dump($house); #object(House)#2 (2) {["name"]=>string(4) "Casa"  ["number"]=>string(1) "7"}

// Прототип
##Кэширование объектов Если объект инициализируется долго (например, загружает данные из БД), его можно клонировать.
##Динамическая конфигурация Объект-прототип хранит настройки, а его копии модифицируются под конкретные задачи.
interface CloneInterface
{
    public function show();
    public function clone();
}

class Prototype implements CloneInterface
{
    public $name;

    public function __construct($name)
    {
        $this->name = $name;
    }
    #возвращает клон самого себя#
    public function clone()
    {
        return clone $this;
    }

    public function show()
    {
        echo "Hello " . $this->name;
    }
}
echo '___Clone___' . "\n";
$original = new Prototype("Vova" . "\n");
$original->show();

$clone = $original->clone();
$clone->name = "Vladimir" . "\n";
$clone->show();

// Одиночка
## глобальный логгер для всего приложения
## кеширование данных
## подключение к базе данных
class Single
{
    private static $close = null;
    private $name;

    #через прайват закрваем доступ на создание напрямую через класс
    private function __construct($name)
    {
        $this->name = $name;
    }

    #получаем экземпляр, только 1#
    public static function GetName($name = null)
    {
        if (self::$close === null) {
            self::$close = new self($name ?? "Default");
        }
        return self::$close;
    }

    public function ShowName()
    {
        echo $this->name;
    }
}
echo '___SingleTone___' . "\n";
$a = Single::GetName("Vova" . "\n");
$a->ShowName();
$a = Single::GetName("Vladimir" . "\n");
$a->ShowName();
