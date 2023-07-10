with profile_sessions as (select PROFILE_ID,
                                 SESSION_ID,
                                 MIN_TS,
                                 MAX_TS,
                                 SESSION_DURATION_MINUTES,
                                 MINUTES_PLAYED_TOTAL,
                                 MINUTES_PLAYED_LEVEL,
                                 MINUTES_PLAYED_LIBRARY,
                                 MINUTES_PLAYED_LSM,
                                 MINUTES_PLAYED_STARLEVEL,
                                 MINUTES_PLAYED_CHALLENGE,
                                 PROFILE_CREATION_TIME
                          from CORE_SP_PROFILE_SESSIONS
                          join CORE_SP_PROFILES using (PROFILE_ID)
--                           where PROFILE_ID = 'PFL6404AB88F38792.24239688')
                          where PROFILE_ID = '$profile_id')
select profile_sessions.SESSION_ID,
       SESSION_DURATION_MINUTES,
       MINUTES_PLAYED_TOTAL,
       MINUTES_PLAYED_LEVEL,
       MINUTES_PLAYED_LIBRARY,
       MINUTES_PLAYED_LSM,
       MINUTES_PLAYED_STARLEVEL,
       MINUTES_PLAYED_CHALLENGE,
       EVENT_TIMESTAMP,
       EVENT_TYPE,
       PARENT_TYPE,
       COURSE_CONTEXT,
       PARENT_NAME,
       ITEM_NAME,
       ITEM_TYPE
from SP_EVENTS_CLEAN
join profile_sessions on (EVENT_TIMESTAMP between min_ts and MAX_TS) and
                         SP_EVENTS_CLEAN.PROFILE_ID = profile_sessions.PROFILE_ID
where 1=1 and
      EVENT_TIMESTAMP > '$profile_creation_timestamp' and
--       EVENT_TIMESTAMP > '2023-03-05 14:47:36.000000000' and
      EVENT_TYPE = 'start' and
      PARENT_TYPE in ('journey_item', 'library', 'lsm')
order by EVENT_TIMESTAMP


-- select * from SP_EVENTS_CLEAN where PROFILE_ID='PFL6404AB88F38792.24239688' and ARRIVAL_TIMESTAMP>'2023-03-05 14:47:36.000000000'
-- order by ARRIVAL_TIMESTAMP