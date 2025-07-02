

# class TriangleChecker:
    
#     def __init__(self,a:int,b:int,c:int):        
#         self.a : int=a
#         self.b : int=b
#         self.c : int=c
#         self.numbers : tuple = [self.a,self.b,self.c]
#     def is_triangle(self)->str:
#         if self.isNotNumber(self.numbers)==False:
#             return "Нужно вводить только числа!"
#         if self.a<=0 or self.b<=0 or self.c<=0:
#             return "С отрицательными числами ничего не выйдет!"
#         if (self.a+self.b>=self.c or self.a+self.c>=self.b or self.c+self.b>=self.a) == 0:
#             return "Жаль, но из этого треугольник не сделать."
#         return "Ура, можно построить треугольник!"
    
#     def isNotNumber(self,numbers:tuple)->bool:
#         for j in range(len(numbers)):
#             if isinstance(numbers[j],str):
#                 return False
#             # for i in range(len(str(abs(numbers[j])))):
#             #     if (str((numbers[j]))[i] in "-0123456789")==False:
#             #         return False
# triangle1 = TriangleChecker(2, 3, 4)
# print(triangle1.is_triangle())
# triangle2 = TriangleChecker(77, 3, 4)
# print(triangle2.is_triangle())
# triangle3 = TriangleChecker(77, 3, 'Сторона3')
# print(triangle3.is_triangle())
# triangle4 = TriangleChecker(77, -3, 4)
# print(triangle4.is_triangle())      
            
# a = TriangleChecker(30,40,50).is_triangle()
# print(a)
# b = TriangleChecker(-30,20,10).is_triangle()
# print(b)
# c = TriangleChecker("ads",20,10).is_triangle()
# print(c)
class Soda:
    def __init__(self, supplement=None):
        if isinstance(supplement, str):
            self.supplement:str = supplement
        else:
            self.supplement = None
    def show_my_drink(self)->str:
        if self.supplement:
            return (f"Газировка и {self.supplement}")
        else:
            return (f"Обычная газировка")


# from abc import ABC, abstractmethod

# def summa(n:int)->int:
#     n = n+1
#     return n 

# class HumanAbstract(ABC):
#     @abstractmethod
#     def show() -> tuple[str,str,int,str,str]:
#         pass
#     def checkGender():
#         pass

# class Human(HumanAbstract):
    
#     maleDictionary : list[str] = ["m", "M"]
#     femaleDictionary : list[str] = ["f", "F"]
    
#     def __init__(self, name:str, sorname:str, age:int, birthday:str, gender:str):
#         self.name : str = name
#         self.sorname : str = sorname
#         self.age : int = age
#         self.birthday : str = birthday
#         self.gender : str = gender
    
#     def show(self) -> tuple[str,str,int,str,str]:
#         return (self.name,self.sorname,self.age,self.birthday,self.gender)    
    
#     def checkGender(self) -> bool:
#         if self.gender in self.maleDictionary:
#             print('you are Male')
#             self.show()
#             return True
#         if self.gender in self.femaleDictionary:
#             print('you are Female')
#             self.show()
#             return True
#         return False
        
#     def checkAge(self):
#         if self.age < 18:
#             pass
            
