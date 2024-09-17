import datetime

from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

now = datetime.datetime.now()

db_string = "postgres://параметры подключения"
db = create_engine(db_string)

SEQUENCE_STEP = 100


def save_rubric_cls(rubricCls):
    Session = sessionmaker(db)
    session = Session()
    base.metadata.create_all(db)
    session.query(RubricCl).delete()

    count_save_rubric = 0
    for rubricCl in rubricCls:
        deleted = rubricCl['Deleted']
        if ('0' != deleted):
            continue

        # Сохранение в БД
        save_rubric_cl(rubricCl, session)
        count_save_rubric += 1

    else:
        session.commit()
        session.close()
        return count_save_rubric
    session.rolback()
    session.close()
    return 0


def save_rubric_cl(rubric_cl, session):
    rubric = RubricCl(theme_id=int(rubric_cl['Isn_node']),
                      theme_value=rubric_cl['Classif_name'],
                      rubric_cod=rubric_cl['Rubric_code'],
                      parent_id=rubric_cl['Isn_high_node'],
                      status_id=1)
    session.add(rubric)


def save_appeals_date(rubric_appeals, date_p, sequence):
    Session = sessionmaker(db)
    session = Session()
    base.metadata.create_all(db)

    for tisRc in rubric_appeals:
        save_appeal_date(tisRc, session, date_p, sequence)
    else:
        session.commit()
        session.close()
        return
    session.rollback()
    session.close()
    return


def save_appeal_date(rubric_appeal, session, date_p, sequence):
    appeal_id = next(sequence)

    appeal = Appeal(service_appeal_id=appeal_id,
                    isn_doc=rubric_appeal['IsnDoc'],
                    reg_num=rubric_appeal['RegNum'],
                    reg_date=rubric_appeal['RegDate'],
                    ogv_name=rubric_appeal['OgvName'],
                    plan_date=rubric_appeal['PlanDate'],
                    fact_date=rubric_appeal['FactDate'],
                    citizen_region=rubric_appeal['Citizen_Region'],
                    kol_zainteres_grazhdan=rubric_appeal['Kol_zainteres_grazhdan'],
                    anonim=rubric_appeal['Anonim'],
                    iscollective=rubric_appeal['Iscollective'],
                    rassm_v_upravl=rubric_appeal['Rassm_v_upravl'],
                    date_p=date_p,
                    date_create=now,
                    ogv_name_cod=rubric_appeal['OgvCode'],
                    citizen_region_cod=rubric_appeal['Citizen_Region_Due'],
                    presledovanie=rubric_appeal['Presledovanie']
                    )
    session.add(appeal)

    if rubric_appeal['TisRubrics'] is not None:
        rubrics = rubric_appeal['TisRubrics']['TisRubric']
        for appeal_question in rubrics:
            save_appeal_question(appeal_question, appeal_id, session, date_p, sequence)


def save_appeal_question(appeal_question, appeal_id, session, date_p, sequence):
    question_id = next(sequence)

    question = AppealQuestion(service_question_id=question_id,
                              service_appeal_id=appeal_id,
                              date_p=date_p,
                              date_create=now,
                              isn_node=appeal_question['Isn_node'],
                              rubriccode=appeal_question['RubricCode'],
                              classifname=appeal_question['ClassifName'],
                              questiontype=appeal_question['QuestionType'],
                              obrgr_predm_vedeniya=appeal_question['obrgr_predm_vedeniya'],
                              zapros_dokumentov=appeal_question['Zapros_dokumentov'],
                              dop_kontrol_upr=appeal_question['Dop_kontrol_upr'],
                              obrgr_res_rassm=appeal_question['obrgr_res_rassm'],
                              eos_sstu_actions=appeal_question['EOS_SSTU_Actions'],
                              ocenka_avtora=appeal_question['Ocenka_avtora'],
                              obrgr_mery_prin_author=appeal_question['obrgr_mery_prin_author'],
                              obrgr_perenapr_v=appeal_question['obrgr_perenapr_v'],
                              obrgr_perenapr_v_ogv=appeal_question['obrgr_perenapr_v_ogv'],
                              ocenkaogvperenapr=appeal_question['OcenkaOgvPerenapr'],
                              obrgr_mery_prin_organ=appeal_question['obrgr_mery_prin_organ']
                              )
    session.add(question)


def get_statistic_save_appeals():
    sql_calculation = "select * from eservice.rog_n_calculation_p()"
    result_execute = db.execute(sql_calculation)
    result_fetchone = result_execute.fetchone()
    result_stat = result_fetchone[0].split()

    return result_stat[0], result_stat[1]


def delete_appeals_date():
    Session = sessionmaker(db)
    session = Session()
    base.metadata.create_all(db)
    session.query(AppealQuestion).delete()
    session.query(Appeal).delete()
    session.commit()
    session.close()

def get_sequence_next_val(sequence_name):
    sql = "select nextval('%s') n" % sequence_name
    result = db.execute(sql)
    n = int(result.fetchone()['n'])
    sql = 'ALTER SEQUENCE %s RESTART WITH %i;' % (sequence_name, (n + SEQUENCE_STEP))
    db.execute(sql)

    return n, n + SEQUENCE_STEP


base = declarative_base()


class RubricCl(base):
    __tablename__ = 'ROG_N_DIC_THEME'

    theme_id = Column(Integer, primary_key=True)
    theme_value = Column(String)
    rubric_cod = Column(String)
    parent_id = Column(Integer)
    date_start = Column(DateTime)
    status_id = Column(Integer)


class Appeal(base):
    __tablename__ = 'ROG_N_SERVICE_APPEAL'

    service_appeal_id = Column(Integer, primary_key=True)
    isn_doc = Column(Integer)
    reg_num = Column(String)
    reg_date = Column(String)
    ogv_name = Column(String)
    plan_date = Column(String)
    fact_date = Column(String)
    citizen_region = Column(String)
    kol_zainteres_grazhdan = Column(Integer)
    anonim = Column(Integer)
    iscollective = Column(Integer)
    rassm_v_upravl = Column(Integer)
    date_p = Column(Date)
    date_create = Column(DateTime)
    ogv_name_cod = Column(String)
    citizen_region_cod = Column(String)
    presledovanie = Column(String)


class AppealQuestion(base):
    __tablename__ = 'ROG_N_SERVICE_QUESTION'

    service_question_id = Column(Integer, primary_key=True)
    service_appeal_id = Column(Integer)
    date_p = Column(Date)
    date_create = Column(DateTime)
    isn_node = Column(Integer)
    rubriccode = Column(String)
    classifname = Column(String)
    questiontype = Column(String)
    obrgr_predm_vedeniya = Column(String)
    zapros_dokumentov = Column(String)
    dop_kontrol_upr = Column(String)
    obrgr_res_rassm = Column(String)
    eos_sstu_actions = Column(String)
    ocenka_avtora = Column(String)
    obrgr_mery_prin_author = Column(String)
    obrgr_perenapr_v = Column(String)
    obrgr_perenapr_v_ogv = Column(String)
    ocenkaogvperenapr = Column(String)
    obrgr_perenapr_v_ogv_id = Column(Integer)
    obrgr_mery_prin_organ = Column(String)


class Sequence:
    def __init__(self, sequence_name):
        self.seqName = sequence_name
        self.seq, self.end_seq = get_sequence_next_val(sequence_name)

    def __iter__(self):
        return self

    def __next__(self):
        if self.end_seq <= self.seq:
            self.seq, self.end_seq = get_sequence_next_val(self.seqName)

        self.seq += 1

        return self.seq
