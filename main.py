import algo_minute


def main():
    #run_minute_average(10,'TSLA')
    algo_minute.run_minute_average_multiple(5,['TSLA','GOOGL','AAPL'],5)

main()