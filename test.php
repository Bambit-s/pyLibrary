<?php

class SingleTone
{
    private static $instance = null;
    private $name;

    // Приватный конструктор запрещает прямое создание объекта
    private function __construct($name)
    {
        $this->name = $name;
    }

    // Единственный способ получить экземпляр
    public static function getInstance($name = null)
    {
        if (self::$instance === null) {
            self::$instance = new self($name ?? 'Default');
        }
        return self::$instance;
    }

    // Запрещаем клонирование
    private function __clone() {}

    // Запрещаем десериализацию
    private function __wakeup() {}

    public function greet()
    {
        return "Hello " . $this->name;
    }
}

// Правильный способ получения экземпляра:
$s = SingleTone::getInstance("Vova");
echo $s->greet(); // Выведет: Hello Vova

// Все последующие вызовы вернут тот же экземпляр
$s2 = SingleTone::getInstance();
echo $s2->greet(); // Тоже выведет: Hello Vova

// Попытка создать новый экземпляр вызовет ошибку:
// $illegal = new SingleTone("Hacker"); // Ошибка!
?>