import numpy as np
from tqdm import tqdm

import pandas as pd
from collections import Counter

class DatasetCounting:
    def __init__(self, csv_path):
        # df = pd.read_csv('Crash Statistics Victoria.csv')
        self.df = pd.read_csv(csv_path)

        # acc_type = list(set(df.ACCIDENT_TYPE.tolist()))
        location_lst = ['LGA_NAME', 'DEG_URBAN_NAME', 'LGA_NAME_ALL', 'SRNS', 'RMA']
        self.crashed_dates = {}


    def load_categories(self):
        crash_dates = sorted(list(set(self.df.ACCIDENT_DATE.tolist())))
        for date in tqdm(crash_dates):
            self.crashed_dates[date] = {}
            acc_dict = self.crashed_dates[date]
            hours = {}
            for i in range(25):
                hours[str(i).zfill(2)] = 0

            acc_day_df = self.df[self.df.ACCIDENT_DATE==date].fillna('')
            acc_periods = sorted(acc_day_df.ACCIDENT_TIME.tolist())
            periods_cnt = Counter(acc_periods)
            acc_dict['total_acc_cnt'] = len(acc_day_df.values.tolist())
            acc_dict['hours'] = periods_cnt

            # ------------ locations
            acc_dict['locations'] = {}
            lga_names = sorted(acc_day_df.LGA_NAME.values.tolist())
            regi_names = sorted(acc_day_df.REGION_NAME.tolist())
            deg_urban_names = sorted(acc_day_df.DEG_URBAN_NAME.tolist())
            srns = sorted(acc_day_df.SRNS.tolist())
            lga_name_cnt = Counter(lga_names)
            regi_cnt = Counter(regi_names)
            deg_cnt = Counter(deg_urban_names)
            srn_cnt = Counter(srns)

            acc_dict['locations']['lga_name'] = lga_name_cnt
            acc_dict['locations']['regi_name'] = regi_cnt
            acc_dict['locations']['deg_urban_name'] = deg_cnt
            acc_dict['locations']['srn'] = srn_cnt

            # ------------ conditions
            acc_dict['conditions'] = {}
            acc_stat = sorted(acc_day_df.ACCIDENT_STATUS.tolist())
            hit_run = sorted(acc_day_df.HIT_RUN_FLAG.tolist())
            light_con = sorted(acc_day_df.LIGHT_CONDITION.tolist())
            police_att = sorted(acc_day_df.POLICE_ATTEND.tolist())
            # injury_stat = sorted(acc_day_df.INJ_OR_FATAL.tolist())
            severity = sorted(acc_day_df.SEVERITY.tolist())
            speed_limit = sorted(acc_day_df.SPEED_ZONE.tolist())


            acc_dict['conditions']['acc_stat'] = Counter(acc_stat)
            acc_dict['conditions']['hit_run'] = Counter(hit_run)
            acc_dict['conditions']['light_con'] = Counter(light_con)
            acc_dict['conditions']['police_att'] = Counter(police_att)
            acc_dict['conditions']['severity'] = Counter(severity)
            acc_dict['conditions']['speed_limit'] = Counter(speed_limit)

            # ------------ collision condition (crash type)
            acc_dict['crash_type'] = {}
            dca_code = sorted(acc_day_df.DCA_CODE.tolist())
            acc_type = sorted(acc_day_df.ACCIDENT_TYPE.tolist())
            node_type = sorted(acc_day_df.NODE_TYPE.tolist())
            acc_dict['crash_type']['dca_code'] = Counter(dca_code)
            acc_dict['crash_type']['acc_type'] = Counter(acc_type)
            acc_dict['crash_type']['node_type'] = Counter(node_type)


            # ------------ road user type
            acc_dict['road_user_type'] = {}
            road_user_df = acc_day_df[['MALES', 'FEMALES', 'BICYCLIST', 'PASSENGER', 'DRIVER',
               'PEDESTRIAN', 'PILLION', 'MOTORIST', 'UNKNOWN', 'PED_CYCLIST_5_12',
               'PED_CYCLIST_13_18', 'OLD_PEDESTRIAN', 'OLD_DRIVER', 'YOUNG_DRIVER']]
            for column in road_user_df:
                column_cnt = Counter(sorted(road_user_df[column].tolist()))
                acc_dict['road_user_type'][column.lower()] = column_cnt

            # ------------ obj hit
            acc_dict['obj_hit'] = {}
            obj_hit_df = acc_day_df[['NO_OF_VEHICLES', 'HEAVYVEHICLE', 'PASSENGERVEHICLE', 'MOTORCYCLE', 'PUBLICVEHICLE']]
            for column in obj_hit_df:
                column_cnt = Counter(sorted(obj_hit_df[column].tolist()))
                acc_dict['obj_hit'][column.lower()] = column_cnt

    def get_category_data(self, date, category):
        return self.crashed_dates[date][category]


if __name__ == '__main__':
    db = DatasetCounting('Crash Statistics Victoria.csv')
    print(db.get_category_data('1/1/2014', 'hours'))