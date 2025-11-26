import os

INIT_CENTURY = [1500, 1600, 1700, 1800]

PROVIDED_DOOMSDAY = [3, 28, 14, 4, 9, 6, 11, 8, 5, 10, 7, 12]

MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

DAYS_IN_YEAR = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class DOOMSDAY:
 
    def __init__(self):
        self.date = None
        self.month = None
        self.year = None
        self.last_two_digit_of_year = None
        self.century = None


    def set_data(self, date, month):
        self.date = date
        self.month = month

    def is_leap_year(self, year):

        self.year = year

        if self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0):
            # Leap year
            DAYS_IN_YEAR[1] = 29
            PROVIDED_DOOMSDAY[0] = 4
            PROVIDED_DOOMSDAY[1] = 29
        else:
            # Not leap year
            DAYS_IN_YEAR[1] = 28
            PROVIDED_DOOMSDAY[0] = 3
            PROVIDED_DOOMSDAY[1] = 28

    def get_century_code(self):

        self.century = (self.year // 100) * 100
        self.last_two_digit_of_year = self.year % 100


        n = self.century % 400

        if n == 300:
            return 3
        elif n == 0:
            return 2
        elif n == 100:
            return 0
        elif n == 200:
            return 5
        else:
            print("Century code calculation failed.")
            os._exit(0) 

    def calculate_doomsday(self, century_code):

        total_number = century_code + self.last_two_digit_of_year // 12 + self.last_two_digit_of_year % 12 + (self.last_two_digit_of_year % 12) // 4
        
        while total_number > 6:
             total_number %= 7

        return total_number  # 0-6
    
    def calculate_day_of_the_week(self, calculated_doomsday):

        try:
            doomsday_for_month = PROVIDED_DOOMSDAY[MONTHS.index(self.month)]

            result = (self.date - doomsday_for_month) % 7 + calculated_doomsday
            result %= 7

            # return result
            return DAYS[result]

        except ValueError:
            return "Invalid month entered.\n"
        
    def get_day_of_the_week(self):

        century_code = self.get_century_code()
        calculated_doomsday = self.calculate_doomsday(century_code)

        return self.calculate_day_of_the_week(calculated_doomsday)
    
    def by_year(self, years):

        start_month = "January" # Start from January
        start_date = 1 # Start from day 1

        temp = []
        temp_month = []
        temp_year = []

        for year in years:

            for month in MONTHS[MONTHS.index(start_month):]:

                self.is_leap_year(year)
       
                for day in range(start_date, DAYS_IN_YEAR[MONTHS.index(month)] + 1):

                    self.set_data(day, month)
                    temp.append(f"{self.get_day_of_the_week()},{day},{month},{year}")
                  
                temp_month.append(temp)
                temp = []
            temp_year.append(temp_month)
            temp_month = []
        
        return temp_year
    

    def by_month(self, year, month):

        return_value =[]
        start_date = 1 # Start from day 1

        self.is_leap_year(year)

        for day in range(start_date, DAYS_IN_YEAR[MONTHS.index(month)] + 1):

            self.set_data(day, month)
            return_value.append(f"{self.get_day_of_the_week()},{day},{month},{year}")


        return return_value
    







def get_data_by_year(years):
        
    calendar = DOOMSDAY()
    
    years = list(map(int, years))
    result = calendar.by_year(years)

    for years in result:

        for printResult in years:
            date_parts = printResult[0].split(',')
            month = date_parts[2]
            year = date_parts[3]

            print("\n","+---",month,"-", year,"---+", "\n")

            for printDates in printResult:
                print(printDates)


# Insert year and month to the constructor
def get_data_by_month(year, month):
        
    calendar = DOOMSDAY()

    result = calendar.by_month(year, month)

    for day in result:
        print(day)



def main():

    get_data_by_year([9999999999999, 2025])
    print("\n---------------------------------------------------\n")
    get_data_by_month(2024, "February")




if __name__ == "__main__":
    main()