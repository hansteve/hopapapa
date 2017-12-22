from src import snowflake




if __name__ == '__main__':

    for i in range(1,100):
        print(snowflake.generate())

    # print(len('{:b}'.format(snowflake.generate())))