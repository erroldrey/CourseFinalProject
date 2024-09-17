import datetime
import logging.config

from apscheduler.schedulers.background import BackgroundScheduler

import ClientService
import DBData
import DateUtils
import MailSender

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("rogSchedulerServiceSedD")

sched = BackgroundScheduler()


def job_function():
    try:
        logger.info('Start loading data in ' + str(datetime.datetime.now()))

        sequence = DBData.Sequence('MON_ID_SEQ')

        count_save_rubric = job_function_rubric_cl()
        count_save_appeal, count_save_question = job_function_appeal_date(sequence)
        logger.info('End loading data in ' + str(datetime.datetime.now()))
        logger.info('Load themes: %s, Load appeal: %s, Load question: %s' %
                    (count_save_rubric, count_save_appeal, count_save_question))

        MailSender.send_email('Data download service: Register appeals',
                              'sherbakov@technocom.tech',
                              'Data upload was successful \n'
                              'Downloaded themes: %s \n'
                              'Downloaded applications: %s \n'
                              'Loaded questions contained in cases: %s' %
                              (count_save_rubric, count_save_appeal, count_save_question))
    except Exception as e:
        logger.error(str(e))


def job_function_rubric_cl():
    rubric_cls = ClientService.get_rubric_cl()
    return DBData.save_rubric_cls(rubric_cls)


def job_function_appeal_date(sequence):
    date_p = DateUtils.get_date_p()
    date_iterator = DateUtils.Period(date_p)
    DBData.delete_appeals_date()
    for x in date_iterator:
        date_from, date_to = x
        rubric_appeals = ClientService.get_appeal_date(date_from, date_to)
        DBData.save_appeals_date(rubric_appeals, date_p, sequence)
    return DBData.get_statistic_save_appeals()


sched.add_job(job_function, 'cron', month='1,4,7,10', day=5, hour=1, minute=1)
sched.start()

# job_function()
