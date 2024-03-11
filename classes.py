import re

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value: str):
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return f'Field: {self.value}'
    
    def __repr__(self):
        return f"Field(value={self.value})"
    
    def __call__(self):
         return self.value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return NotImplemented
        return self.value == __value

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return NotImplemented
        return self.value < __value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return NotImplemented
        return self.value > __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return NotImplemented
        return self.value <= __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Field):
            return NotImplemented
        return self.value >= __value


class Name(Field):
    def __init__(self, value: str):
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if len(value.lstrip()):
            self.__value = value
        else:
            raise ValueError('Error: The entered contact name is empty.\n')

    def __str__(self):
        return f'Name: {self.value}'
    
    def __repr__(self):
        return f"Name(value={self.value})"
    
    def __call__(self):
        return self.value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Name):
            return NotImplemented
        return self.value == __value.value

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Name):
            return NotImplemented
        return self.value < __value.value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Name):
            return NotImplemented
        return self.value > __value.value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Name):
            return NotImplemented
        return self.value <= __value.value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Name):
            return NotImplemented
        return self.value >= __value.value


class Phone(Field):
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.fullmatch(r'\d{10}', value):
            self.__value = value
        else:
            raise ValueError (f'Error: The number of digits in the number does not correspond to 10: {value}\n')
    
    @classmethod
    def validation(cls, value: str):
        if value:
            cls.__validation(cls, value)
            if cls.value:
                return value
        return False
    
    def __validation(self, value: str):
        self.__value = None
        if re.fullmatch(r'\d{10}', value):
            self.__value = value
        else:
            raise ValueError (f'Error: The number of digits in the number does not correspond to 10.{value}\n')
        
    def __str__(self):
        return f'Phone: {self.value}'
    
    def __repr__(self) -> str:
        return f"Phone(value={self.value})"
    
    def __call__(self):
        return self()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Phone):
            return NotImplemented
        return self.value == __value.value

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Phone):
            return NotImplemented
        return self.value < __value.value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Phone):
            return NotImplemented
        return self.value > __value.value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Phone):
            return NotImplemented
        return self.value <= __value.value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Phone):
            return NotImplemented
        return self.value >= __value.value


class Birthday(Field):
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            if value:
                self.__value = datetime.strptime(value, '%d.%m.%Y').strftime('%d.%m.%Y')
            else:
                self.__value = None
        except ValueError:
            raise ValueError("Error: Invalid date format. Use DD.MM.YYYY\n")

    @classmethod
    def validation(cls, value: str):
        return cls.__validation(value)
    
    def __validation(self, value: str):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            return date_birthday.strftime('%d.%m.%Y')
        except ValueError:
            raise ValueError("Error: Invalid date format. Use DD.MM.YYYY\n")

    def __str__(self):
        return f"Birthday: {self.value}"
    
    def __repr__(self) -> str:
        return f"Birthday(value={self.value} (format='%d.%m.%Y'))"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Birthday):
            return NotImplemented
        return self.value == __value.value

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Birthday):
            return NotImplemented
        return self.value < __value.value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Birthday):
            return NotImplemented
        return self.value > __value.value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Birthday):
            return NotImplemented
        return self.value <= __value.value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Birthday):
            return NotImplemented
        return self.value >= __value.value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.__birthday = None
    
    @property
    def name(self):
        return self.__name
        
    @name.setter
    def name(self, value):
        if isinstance(value, Name):
            self.__name = value
        else:
            self.__name = Name(str(value))


    @property
    def birthday(self):
        return self.__birthday
        
    @birthday.setter
    def birthday(self, value: str):
        self.__birthday = Birthday(value)
    
    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        if not new_phone in self.phones:
            self.phones.append(new_phone)
        else:
            raise ValueError('Warning: The contact contains a number.\n')
    
    def remove_phone(self, phone: str):
        self.phones.remove(Phone(phone))
    
    def edit_phone(self, phone: str, new_phone: str):
        _phone = Phone(phone)
        _new_phone = Phone(new_phone)
        if self.find_phone(new_phone):
            raise ValueError(f'{new_phone} is in the list of numbers of the contact.\n')
        elif self.find_phone(phone):
            self.phones = list(map(lambda item: _new_phone if item == _phone else item, self.phones))
        else:
            raise ValueError(f"{phone} is'n in the list of numbers of the contact.\n")
   
    def find_phone(self, user_phone: str) -> Phone:
        _user_phone = Phone(user_phone)
        if user_phone:
            #found_phone = self.phones[self.phones.index(_user_phone)]
            found_phone = list(filter(lambda phone: phone==_user_phone, self.phones))
            return found_phone
        return None
    
    def add_birthday(self, birthday: str):
        self.__birthday = Birthday(birthday)
    
    def __call__(self) -> Name:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Record):
            return NotImplemented
        if not (self.name == other.name):
            return  False
        if not (len(self.phone) == len(other.phones)):
            return  False
        if not (self.birthday == other.birthday):
            return False
        if not self.phones == other.phones:
            return False

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def __str__(self):
        return f"Record a contact: {self.name}, \
phones: {'; '.join(p.value for p in self.phones)} \
birthday: {self.birthday.value if self.birthday else 'format=DD.MM.YYYY'}\n"
    
    def __repr__(self):
        return f"Record(value={self.name}, \
phones={'; '.join(p.value for p in self.phones)}, \
birthday={self.birthday.value if self.birthday else 'format(%d.%m.%Y)'}\n"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        if not isinstance(record, Record):
            return NotImplemented
        if record.name.value in self.data:
            raise ValueError('Warning: Contact exists.\n')
        else:
            self.data[record.name.value] = record
    
    def find(self, name: str) -> Record:
        if name:
            if name in self.data:
                return self.data[name]
            return None
        raise ValueError('Error: Contact name is empty.\n')
    
    def delete(self, name: str):
        self.data.pop(name)
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        for record in self.data.values():
            buffer_record = Record(record.name.value)
            # The 'buffer_record' is needed to keep the original date.
            try:
                now_date = datetime.today().date()
                date_user =  datetime.strptime(record.birthday.value, '%d.%m.%Y').replace(now_date.year).date()
                dates_differences = (date_user - now_date).days

                if dates_differences <= 7 and dates_differences >= 0:
                    if date_user.weekday() == 6:
                        buffer_record.add_birthday((date_user + timedelta(days = 1)).strftime('%d.%m.%Y'))
                    elif date_user.weekday() == 5:
                        buffer_record.add_birthday((date_user + timedelta(days = 2)).strftime('%d.%m.%Y'))
                    else:
                        buffer_record.add_birthday(date_user.strftime('%d.%m.%Y'))

                    upcoming_birthdays.append({record.name.value : record.birthday.value})
            except:
                upcoming_birthdays.append({record.name.value: ''})
        return upcoming_birthdays