import threading


INIT_CENTURY = [1500, 1600, 1700, 1800]

DAYS_IN_YEAR = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

PROVIDED_DOOMSDAY = [3, 28, 14, 4, 9, 6, 11, 8, 5, 10, 7, 12]

MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]




class DOOMSDAY_OF_THE_YEAR:
    def __init__(self):
        self.year = None
        self.stop_threads = threading.Event()  # Shared event to signal threads to stop
        self.doomsday_century_code = None

    # Calculate the century code: 2024 -> 2000
    # (1500, 1600, 1700, 1800) += 400 is equal to 2000 or not
    # (1500 = 3, 1600 = 2, 1700 = 0,1800 = 5)
    def calculate_century_code(self, init_century):
        doomsday_century_temp = init_century

        digitCount = len(str(abs(self.year)))
        digitCountLastTwo = digitCount - 2

        while not self.stop_threads.is_set():
            if doomsday_century_temp == int(str(self.year)[:digitCountLastTwo]) * (10 ** digitCountLastTwo):
               
                if init_century == INIT_CENTURY[0]: # 1500
                    self.doomsday_century_code = 3
                elif init_century == INIT_CENTURY[1]: # 1600
                    self.doomsday_century_code = 2
                elif init_century == INIT_CENTURY[2]: #1700
                    self.doomsday_century_code = 0
                elif init_century == INIT_CENTURY[3]: # 1800
                    self.doomsday_century_code = 5
                else:
                    self.doomsday_century_code = None

                self.stop_threads.set()  # Signal other threads to stop
                return  # Exit the loop and thread
            else:
                doomsday_century_temp += 400

    # Calculate the century code by using threads
    def get_century_code(self):
        
        threads = []

        for init_century in INIT_CENTURY:
            thread = threading.Thread(
                target=self.calculate_century_code,
                args=(init_century,)  # Pass args as a tuple
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return self.doomsday_century_code


    # This functiopn will calculate for the doomsday of that year (Jan.-Dec.)
    def calculate_doomsday_year(self):

        digitCount = len(str(abs(self.year)))
        digitCountLastTwo = digitCount - 2

        twoYearAfterCentury = int(str(self.year)[digitCountLastTwo:digitCount])

        # get_century_code is threading function
        # calculate_century_code is the real function of getting the century code
        century_code = self.get_century_code()

        if century_code is None:
            raise ValueError("Century code calculation failed.")

        total_number = century_code + twoYearAfterCentury // 12 + twoYearAfterCentury % 12 + (twoYearAfterCentury % 12) // 4

        while total_number > 6:
            total_number %= 7

        return total_number  # 0-6

    # Find if that year is leap year or not
    def is_leap_year(self):

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





class DAY_OF_THE_WEEK(DOOMSDAY_OF_THE_YEAR):
    def __init__(self):
        super().__init__()
        self.month = None
        self.date = None
        self.calculated_doomsday = None

    # Recalculate after the year has been set by calling
    # DOOMSDAY_OF_THE_YEAR -> calculate_doomsday_year()
    def set_year(self, year):
        self.year = year
        self.stop_threads.clear()
        self.doomsday_century_code = None
        super().is_leap_year()
        self.calculated_doomsday = self.calculate_doomsday_year()

    # Reduce time complexity by using all the consttructors
    # in DAY_OF_THE_WEEK for that year
    def set_date(self, month, date):
        self.month = month
        self.date = date

    # This function will calculate for
    # the day of the week of that date
    def calculate_day_of_the_week(self):

        try:
            doomsday_for_month = PROVIDED_DOOMSDAY[MONTHS.index(self.month)]

            result = (self.date - doomsday_for_month) % 7 + self.calculated_doomsday
            result %= 7

            # return result
            return DAYS[result]

        except ValueError:
            return "Invalid month entered.\n"
       
        
    def by_year(self, years):

        temp = []
        temp_month = []
        temp_year = []

        for year in years:

            month = "January" # Start from January
            start_date = 1 # Start from day 1

            self.set_year(year)

            for month in MONTHS[MONTHS.index(month):]:
       

                for day in range(start_date, DAYS_IN_YEAR[MONTHS.index(month)] + 1):

                    self.set_date(month, day)
                    temp.append(f"{self.calculate_day_of_the_week()},{day},{month},{year}")
                  
                temp_month.append(temp)
                temp = []
            temp_year.append(temp_month)
            temp_month = []

        
        return temp_year
    

    def by_month(self, year, month):

        return_value =[]
        start_date = 1 # Start from day 1

        self.set_year(year[0])

        for day in range(start_date, DAYS_IN_YEAR[MONTHS.index(month)] + 1):

            self.set_date(month, day)
            return_value.append(f"{self.calculate_day_of_the_week()},{day},{month},{year[0]}")

        return return_value
    







def insert_data_by_year(years):
        
        years = list(map(int, years))

        calendar = DAY_OF_THE_WEEK()
        result = calendar.by_year(years)

        return result


# Insert year and month to the constructor
def insert_data_by_month(year, month):
        
        years = list(map(int, year))

        calendar = DAY_OF_THE_WEEK()
        result = calendar.by_month(years, month)

        return result





from datetime import datetime

def main():

    start_time = datetime.now()
    print(f"\nStart time: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
    print("Calculating...")

    # Uncomment one
    result = insert_data_by_year([2024, 2025]) # or [2023],[2024],[2025]  
    # result = insert_data_by_month([2024], "April")


    stop_time_procss = datetime.now()


    for years in result:

        for printResult in years:
            date_parts = printResult[0].split(',')
            month = date_parts[2]
            year = date_parts[3]

            print("\n","+---",month,"-", year,"---+", "\n")

            for printDates in printResult:
                print(printDates)

    stop_time = datetime.now()

    print(f"\nStart time:                               {start_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Stop time:                                {stop_time_procss.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Stop time (excludes calculation process): {stop_time.strftime('%H:%M:%S.%f')[:-3]}\n")

    durationP = stop_time_procss - start_time
    totalDuration = stop_time - start_time

    print(f"Duration :                                {durationP}")
    print(f"Duration (excludes calculation process):  {totalDuration}\n")



if __name__ == "__main__":
    main()