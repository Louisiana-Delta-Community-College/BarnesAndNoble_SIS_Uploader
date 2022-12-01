from Config import _TIME_FRAME, _EMAIL_DOMAIN, _EMAIL_DOMAIN_WITH_EXT, _EMAIL_DOMAIN_ADJUNCT_WITH_EXT

_strSQLCourses = """
select
    "recordNumber",
    "campus",
    "school",
    "institutionDepartment", 
    "term",                        
    "department",                  
    "course",                      
    "section",        
    "campusTitle",                 
    "schoolTitle",                    -- conditional. references optional "school". Opting out.
    case
      when "institutionDepartment" is not null then "institutionDepartment"||' Department' 
    end "institutionDepartmentTitle", -- conditional. references optional "institutionDepartment".
    "courseTitle",                    -- required. human readable title for the "course" field
    "institutionCourseCode",       
    "institutionClassCode",           -- recommended; not required
    "institutionSubjectCodes",        -- recommended; not required
    "institutionSubjectsTitle",       -- recommended; not required
    "crn",                         
    "termTitle",                   
    "termType",                    
    "termStartDate",               
    "termEndDate",                 
    "sectionStartDate",            
    "sectionEndDate",              
    "classGroupId",                   -- not required
    "estimatedEnrollment"
from (
  select
      ROW_NUMBER() OVER (
        ORDER BY ssbsect.ssbsect_camp_code
      )                                       "recordNumber",
      ssbsect.ssbsect_camp_code               "campus",
      ''                                      "school",                      -- optional
      case 
        when stvdept.stvdept_desc is not null then stvdept.stvdept_desc
        else
          case 
          
            /* BUSINESS COURSE(S) */
            when ssbsect.ssbsect_subj_code    = 'ACCT'
              OR ssbsect.ssbsect_subj_code    = 'BUSE'
              OR ssbsect.ssbsect_subj_code    = 'BMET'
              OR ssbsect.ssbsect_subj_code    = 'BOTH'
              OR ssbsect.ssbsect_subj_code    = 'BOTL'
              OR ssbsect.ssbsect_subj_code    = 'BTEL'
              OR ssbsect.ssbsect_subj_code    = 'BUSI'
              OR ssbsect.ssbsect_subj_code    = 'BUSM'
              OR ssbsect.ssbsect_subj_code    = 'BUSN'
              OR ssbsect.ssbsect_subj_code    = 'CADD'
              OR ssbsect.ssbsect_subj_code    = 'CCRV'
              OR ssbsect.ssbsect_subj_code    = 'CINS'
              OR ssbsect.ssbsect_subj_code    = 'CISX'
              OR ssbsect.ssbsect_subj_code    = 'CNCS'
              OR ssbsect.ssbsect_subj_code    = 'CNET'
              OR ssbsect.ssbsect_subj_code    = 'COMP'
              OR ssbsect.ssbsect_subj_code    = 'CPTR'
              OR ssbsect.ssbsect_subj_code    = 'CSCI'
              OR ssbsect.ssbsect_subj_code    = 'CSRV'
              OR ssbsect.ssbsect_subj_code    = 'ECON'
              OR ssbsect.ssbsect_subj_code    = 'ENTP'
              OR ssbsect.ssbsect_subj_code    = 'ETRN'
              OR ssbsect.ssbsect_subj_code    = 'HURM'
              OR ssbsect.ssbsect_subj_code    = 'IDEL'
              OR ssbsect.ssbsect_subj_code    = 'INCT'
              OR ssbsect.ssbsect_subj_code    = 'INTE'
              OR ssbsect.ssbsect_subj_code    = 'ISYS'
              OR ssbsect.ssbsect_subj_code    = 'KYBD'
              OR ssbsect.ssbsect_subj_code    = 'MACH'
              OR ssbsect.ssbsect_subj_code    = 'MAST'
              OR ssbsect.ssbsect_subj_code    = 'MATR'
              OR ssbsect.ssbsect_subj_code    = 'MCS'	
              OR ssbsect.ssbsect_subj_code    = 'MEDL'
              OR ssbsect.ssbsect_subj_code    = 'MGMT'
              OR ssbsect.ssbsect_subj_code    = 'ORNT'
              OR ssbsect.ssbsect_subj_code    = 'OSYS'
            then 'Business'
            
            /* INDUSTRIAL TECHNOLOGY COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'AUTO'
              OR ssbsect.ssbsect_subj_code = 'CARP'
              OR ssbsect.ssbsect_subj_code = 'CTDP'
              OR ssbsect.ssbsect_subj_code = 'DPET'
              OR ssbsect.ssbsect_subj_code = 'DRFT'
              OR ssbsect.ssbsect_subj_code = 'ELEC'
              OR ssbsect.ssbsect_subj_code = 'ELTR'
              OR ssbsect.ssbsect_subj_code = 'HACR'
              OR ssbsect.ssbsect_subj_code = 'HVAC'
              OR ssbsect.ssbsect_subj_code = 'IMFG'
              OR ssbsect.ssbsect_subj_code = 'IMMT'
              OR ssbsect.ssbsect_subj_code = 'INST'
              OR ssbsect.ssbsect_subj_code = 'JOBS'
              OR ssbsect.ssbsect_subj_code = 'PTEC'
              OR ssbsect.ssbsect_subj_code = 'SOLR'
              OR ssbsect.ssbsect_subj_code = 'SPPR'
              OR ssbsect.ssbsect_subj_code = 'WELD'
            then 'Industrial Technology'
            
            /* LIBERAL ARTS COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'ACSE' 
              OR ssbsect.ssbsect_subj_code = 'ARTS'
              OR ssbsect.ssbsect_subj_code = 'CDYC'
              OR ssbsect.ssbsect_subj_code = 'CJUS'
              OR ssbsect.ssbsect_subj_code = 'EDUC'
              OR ssbsect.ssbsect_subj_code = 'ENGL'
              OR ssbsect.ssbsect_subj_code = 'FORS'
              OR ssbsect.ssbsect_subj_code = 'FREN'
              OR ssbsect.ssbsect_subj_code = 'FRST'
              OR ssbsect.ssbsect_subj_code = 'GEOG'
              OR ssbsect.ssbsect_subj_code = 'HIST'
              OR ssbsect.ssbsect_subj_code = 'HPER'
              OR ssbsect.ssbsect_subj_code = 'HUMN'
              OR ssbsect.ssbsect_subj_code = 'JJSP'
              OR ssbsect.ssbsect_subj_code = 'MCSM'
              OR ssbsect.ssbsect_subj_code = 'MILS'
              OR ssbsect.ssbsect_subj_code = 'MUSC'
              OR ssbsect.ssbsect_subj_code = 'PHIL'
              OR ssbsect.ssbsect_subj_code = 'POLI'
              OR ssbsect.ssbsect_subj_code = 'PSYC'
              OR ssbsect.ssbsect_subj_code = 'READ'
              OR ssbsect.ssbsect_subj_code = 'SOCL'
              OR ssbsect.ssbsect_subj_code = 'SPAN'
              OR ssbsect.ssbsect_subj_code = 'SPCH'
              OR ssbsect.ssbsect_subj_code = 'SPCM'
              OR ssbsect.ssbsect_subj_code = 'TEAC'
              OR ssbsect.ssbsect_subj_code = 'THEA'
            then 'Liberal Arts'
            
            when ssbsect.ssbsect_subj_code = 'BIOL'
              OR ssbsect.ssbsect_subj_code = 'CHEM'
              OR ssbsect.ssbsect_subj_code = 'GEOL'
              OR ssbsect.ssbsect_subj_code = 'MATH'
              OR ssbsect.ssbsect_subj_code = 'PHSC'
              OR ssbsect.ssbsect_subj_code = 'PHYS'
              OR ssbsect.ssbsect_subj_code = 'SCIE'
            then 'Natural Science &' || ' Math'
            
            /* ALLIED HEALTH COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'AHEN'
              OR ssbsect.ssbsect_subj_code = 'AHMA'
              OR ssbsect.ssbsect_subj_code = 'AHRE'
              OR ssbsect.ssbsect_subj_code = 'AHSC'
              OR ssbsect.ssbsect_subj_code = 'BARB'
              OR ssbsect.ssbsect_subj_code = 'EMSE'
              OR ssbsect.ssbsect_subj_code = 'EMTP'
              OR ssbsect.ssbsect_subj_code = 'HCOR'
              OR ssbsect.ssbsect_subj_code = 'HEHS'
              OR ssbsect.ssbsect_subj_code = 'HEKG'
              OR ssbsect.ssbsect_subj_code = 'HEMS'
              OR ssbsect.ssbsect_subj_code = 'HIM'
              OR ssbsect.ssbsect_subj_code = 'HMDT'
              OR ssbsect.ssbsect_subj_code = 'HNUR'
              OR ssbsect.ssbsect_subj_code = 'HPHL'
              OR ssbsect.ssbsect_subj_code = 'HSCI'
              OR ssbsect.ssbsect_subj_code = 'HSPR'
            then 'Allied Health'
            
            /* NURSING COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'NRSA'
              OR ssbsect.ssbsect_subj_code = 'NURS'
            then 'Nursing'
            
            /* REG OFF COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'ABST' then 'Reg Off'
            
            /* STUDENT SERVICES COURSE(S) */
            when ssbsect.ssbsect_subj_code = 'PWPL' then 'Student Services'          
  
        end 
      end "institutionDepartment", 
      ssbsect.ssbsect_term_code               "term",                        
      ssbsect.ssbsect_subj_code               "department",                  
      ssbsect.ssbsect_crse_numb               "course",                      
      ssbsect.ssbsect_crn                     "section",        
      /* ssbsect.ssbsect_seq_numb                "section", */ 
      stvcamp.stvcamp_desc                    "campusTitle",                 
      ''                                      "schoolTitle",                 -- conditional. references optional "school". Opting out.
      stvdept.stvdept_desc||' Department'     "institutionDepartmentTitle",  -- conditional. references optional "institutionDepartment".
      ct.crse_title                           "courseTitle",                 -- required. human readable title for the "course" field
      ssbsect.ssbsect_subj_code||' '||                                       
      ssbsect.ssbsect_crse_numb               "institutionCourseCode",       
      ssbsect.ssbsect_subj_code||' '||                                       
      ssbsect.ssbsect_crse_numb||' '||                                                                            
      ssbsect.ssbsect_crn                     "institutionClassCode",        -- recommended; not required
      ''                                      "institutionSubjectCodes",     -- recommended; not required
      stvsubj.stvsubj_desc                    "institutionSubjectsTitle",    -- recommended; not required
      ssbsect.ssbsect_crn                     "crn",                         
      stvterm.stvterm_desc                    "termTitle",                   
      'Term'                                  "termType",                    
      to_char(
        (cast(stvterm.stvterm_start_date as timestamp) at time zone 'UTC'),
        'YYYY-MM-DD"T"HH24:MM:SSxFF3"Z"'
      )                                       "termStartDate",               
      to_char(
        (cast(stvterm.stvterm_end_date as timestamp) at time zone 'UTC'), 
        'YYYY-MM-DD"T"HH24:MM:SSxFF3"Z"'
      )                                       "termEndDate",                 
      to_char(
        (cast(ssbsect.ssbsect_ptrm_start_date as timestamp) at time zone 'UTC'),
        'YYYY-MM-DD"T"HH24:MM:SSxFF3"Z"'
      )                                       "sectionStartDate",            
      to_char(
        (cast(ssbsect.ssbsect_ptrm_end_date as timestamp) at time zone 'UTC'), 
        'YYYY-MM-DD"T"HH24:MM:SSxFF3"Z"'
      )                                       "sectionEndDate",              
      ''                                      "classGroupId",                -- not required
      ssbsect.ssbsect_max_enrl                "estimatedEnrollment"
  from ssbsect
  
  join stvcamp on stvcamp.stvcamp_code        = ssbsect.ssbsect_camp_code
  
  left join stvdept on stvdept.stvdept_code   = ssbsect.ssbsect_subj_code
  
  join stvsubj on stvsubj.stvsubj_code        = ssbsect.ssbsect_subj_code
  
  join stvterm on stvterm.stvterm_code        = ssbsect.ssbsect_term_code
  
  join (
      select
          scbcrse.scbcrse_subj_code subj_code,
          scbcrse.scbcrse_crse_numb crse_numb,
          scbcrse.scbcrse_title     crse_title
      from scbcrse
      join (
          select
              scbcrse.scbcrse_subj_code subj_code,
              scbcrse.scbcrse_crse_numb crse_numb,
              max(scbcrse.scbcrse_activity_date) md
          from scbcrse
          group by
              scbcrse.scbcrse_subj_code,
              scbcrse.scbcrse_crse_numb
      ) maxd on maxd.subj_code = scbcrse.scbcrse_subj_code
            and maxd.crse_numb = scbcrse.scbcrse_crse_numb
            and maxd.md        = scbcrse.scbcrse_activity_date
  ) ct on ct.subj_code = ssbsect.ssbsect_subj_code
      and ct.crse_numb = ssbsect.ssbsect_crse_numb
  where {_TIME_FRAME}
)
""".format(**locals())

_strSQLEnrollments = """
select 
    ROW_NUMBER() OVER (
		ORDER BY main."pidm"
	) 										        "recordNumber",
    main."campus", 
    main."school", 
    case 
      when main."institutionDepartment" is not null then main."institutionDepartment"
      else
        case 
        
          /* BUSINESS COURSE(S) */
          when main."department"  = 'ACCT'
            OR main."department"    = 'BUSE'
            OR main."department"    = 'BMET'
            OR main."department"    = 'BOTH'
            OR main."department"    = 'BOTL'
            OR main."department"    = 'BTEL'
            OR main."department"    = 'BUSI'
            OR main."department"    = 'BUSM'
            OR main."department"    = 'BUSN'
            OR main."department"    = 'CADD'
            OR main."department"    = 'CCRV'
            OR main."department"    = 'CINS'
            OR main."department"    = 'CISX'
            OR main."department"    = 'CNCS'
            OR main."department"    = 'CNET'
            OR main."department"    = 'COMP'
            OR main."department"    = 'CPTR'
            OR main."department"    = 'CSCI'
            OR main."department"    = 'CSRV'
            OR main."department"    = 'ECON'
            OR main."department"    = 'ENTP'
            OR main."department"    = 'ETRN'
            OR main."department"    = 'HURM'
            OR main."department"    = 'IDEL'
            OR main."department"    = 'INCT'
            OR main."department"    = 'INTE'
            OR main."department"    = 'ISYS'
            OR main."department"    = 'KYBD'
            OR main."department"    = 'MACH'
            OR main."department"    = 'MAST'
            OR main."department"    = 'MATR'
            OR main."department"    = 'MCS'	
            OR main."department"    = 'MEDL'
            OR main."department"    = 'MGMT'
            OR main."department"    = 'ORNT'
            OR main."department"    = 'OSYS'
          then 'Business'
          
          /* INDUSTRIAL TECHNOLOGY COURSE(S) */
          when main."department" = 'AUTO'
            OR main."department" = 'CARP'
            OR main."department" = 'CTDP'
            OR main."department" = 'DPET'
            OR main."department" = 'DRFT'
            OR main."department" = 'ELEC'
            OR main."department" = 'ELTR'
            OR main."department" = 'HACR'
            OR main."department" = 'HVAC'
            OR main."department" = 'IMFG'
            OR main."department" = 'IMMT'
            OR main."department" = 'INST'
            OR main."department" = 'JOBS'
            OR main."department" = 'PTEC'
            OR main."department" = 'SOLR'
            OR main."department" = 'SPPR'
            OR main."department" = 'WELD'
          then 'Industrial Technology'
          
          /* LIBERAL ARTS COURSE(S) */
          when main."department"   = 'ACSE' 
            OR main."department" = 'ARTS'
            OR main."department" = 'CDYC'
            OR main."department" = 'CJUS'
            OR main."department" = 'EDUC'
            OR main."department" = 'ENGL'
            OR main."department" = 'FORS'
            OR main."department" = 'FREN'
            OR main."department" = 'FRST'
            OR main."department" = 'GEOG'
            OR main."department" = 'HIST'
            OR main."department" = 'HPER'
            OR main."department" = 'HUMN'
            OR main."department" = 'JJSP'
            OR main."department" = 'MCSM'
            OR main."department" = 'MILS'
            OR main."department" = 'MUSC'
            OR main."department" = 'PHIL'
            OR main."department" = 'POLI'
            OR main."department" = 'PSYC'
            OR main."department" = 'READ'
            OR main."department" = 'SOCL'
            OR main."department" = 'SPAN'
            OR main."department" = 'SPCH'
            OR main."department" = 'SPCM'
            OR main."department" = 'TEAC'
            OR main."department" = 'THEA'
          then 'Liberal Arts'
          
          when main."department" = 'BIOL'
            OR main."department" = 'CHEM'
            OR main."department" = 'GEOL'
            OR main."department" = 'MATH'
            OR main."department" = 'PHSC'
            OR main."department" = 'PHYS'
            OR main."department" = 'SCIE'
          then 'Natural Science &' || ' Math'
          
          /* ALLIED HEALTH COURSE(S) */
          when main."department" = 'AHEN'
            OR main."department" = 'AHMA'
            OR main."department" = 'AHRE'
            OR main."department" = 'AHSC'
            OR main."department" = 'BARB'
            OR main."department" = 'EMSE'
            OR main."department" = 'EMTP'
            OR main."department" = 'HCOR'
            OR main."department" = 'HEHS'
            OR main."department" = 'HEKG'
            OR main."department" = 'HEMS'
            OR main."department" = 'HIM'
            OR main."department" = 'HMDT'
            OR main."department" = 'HNUR'
            OR main."department" = 'HPHL'
            OR main."department" = 'HSCI'
            OR main."department" = 'HSPR'
          then 'Allied Health'
          
          /* NURSING COURSE(S) */
          when main."department" = 'NRSA'
            OR main."department" = 'NURS'
          then 'Nursing'
          
          /* REG OFF COURSE(S) */
          when main."department" = 'ABST' then 'Reg Off'
          
          /* STUDENT SERVICES COURSE(S) */
          when main."department" = 'PWPL' then 'Student Services'          

      end 
    end "institutionDepartment", 
    main."term", 
    main."department", 
    main."course", 
    main."section",
    main."email", 
    main."firstName", 
    main."middleName", 
    main."lastName", 
    main."userRole", 
    main."sisUserId", 
    main."includedInCourseFee", 
    main."studentFullPartTimeStatus", 
    main."creditHours"
from (
    (
        select
            sfrstcr.sfrstcr_pidm                    "pidm",
            ssbsect.ssbsect_camp_code               "campus",
            ''                                      "school",                         -- optional
            stvdept.stvdept_desc                    "institutionDepartment",          -- optional
            ssbsect.ssbsect_term_code               "term",                        
            ssbsect.ssbsect_subj_code               "department",                  
            ssbsect.ssbsect_crse_numb               "course",                      
            ssbsect.ssbsect_crn                     "section",                     
            /* ssbsect.ssbsect_seq_numb                "section", */   
            case
                when lower(preferred.email) like '%{_EMAIL_DOMAIN}%' then preferred.email
                when lower(most_recent_active.email) like '%{_EMAIL_DOMAIN}%' then most_recent_active.email
                when preferred.email is not null then preferred.email
                when most_recent_active.email is not null then most_recent_active.email
                else lower(spriden.spriden_first_name||spriden.spriden_last_name||'@{_EMAIL_DOMAIN_ADJUNCT_WITH_EXT}')
            end                                     "email",
            spriden.spriden_first_name              "firstName",
            spriden.spriden_mi                      "middleName",
            spriden.spriden_last_name               "lastName",
            'Student'                               "userRole",
			to_char(spriden.spriden_pidm)           "sisUserId",					  -- conditional; required if "userRole" is "Student"
            'N'                                     "includedInCourseFee",            -- conditional; Required if "userRole" is "Student"
            ftpt.ftpt_status                        "studentFullPartTimeStatus",
            to_char(sfrstcr.sfrstcr_credit_hr)      "creditHours"
        from sfrstcr
        
        join spriden 
        on spriden.spriden_pidm        = sfrstcr.sfrstcr_pidm
        and spriden.spriden_change_ind is null
        
        join ssbsect 
        on ssbsect.ssbsect_crn         = sfrstcr.sfrstcr_crn
        and ssbsect.ssbsect_term_code  = sfrstcr.sfrstcr_term_code
        
        left join stvdept on stvdept.stvdept_code   = ssbsect.ssbsect_subj_code
        
        join stvterm on stvterm.stvterm_code        = ssbsect.ssbsect_term_code
        
        /* Full Time / Part Time status */
        join (
            select
                pidm,
                term,
                case
                    when sum_hr < 12 then 'P'
                    when sum_hr is null then 'P'
                    when sum_hr >= 12 then 'F'
                end ftpt_status
            from (
                select
                    sfrstcr.sfrstcr_pidm pidm,
                    sfrstcr.sfrstcr_term_code term,
                    sum(sfrstcr.sfrstcr_credit_hr) sum_hr
                from sfrstcr
                where sfrstcr.sfrstcr_rsts_code in ('RE', 'RW')
                group by
                    sfrstcr.sfrstcr_pidm,
                    sfrstcr.sfrstcr_term_code
            )
        ) ftpt on ftpt.pidm                         = sfrstcr.sfrstcr_pidm
            and ftpt.term                         = sfrstcr.sfrstcr_term_code
        
        /* preferred email */
        left join (
            select 
                goremal.goremal_pidm pidm,
                goremal.goremal_email_address email
            from goremal 
            where goremal.goremal_preferred_ind = 'Y'
            and goremal.goremal_status_ind    = 'A'
        ) preferred on preferred.pidm               = sfrstcr.sfrstcr_pidm
        
        /* most recent active email */
        left join (
            select 
                goremal.goremal_pidm pidm,
                goremal.goremal_email_address email
            from goremal 
            join (
                select
                    goremal.goremal_pidm pidm,
                    max(goremal.goremal_activity_date) md
                from goremal
                where goremal.goremal_status_ind = 'A' 
                group by
                    goremal.goremal_pidm
            ) maxd on maxd.pidm = goremal.goremal_pidm
                and maxd.md   = goremal.goremal_activity_date
            where goremal.goremal_status_ind    = 'A'
        ) most_recent_active on most_recent_active.pidm               = sfrstcr.sfrstcr_pidm
        where sfrstcr.sfrstcr_rsts_code            in ('RE', 'RW')
        and {_TIME_FRAME}
    ) union (
        select
            instructors.pidm                        "pidm",
            ssbsect.ssbsect_camp_code               "campus",
            ''                                      "school",                         -- optional
            stvdept.stvdept_desc                    "institutionDepartment",          -- optional
            ssbsect.ssbsect_term_code               "term",                        
            ssbsect.ssbsect_subj_code               "department",                  
            ssbsect.ssbsect_crse_numb               "course",                      
            ssbsect.ssbsect_crn                     "section",                
            /* ssbsect.ssbsect_seq_numb                "section", */   
            case
                when lower(preferred.email) like '%{_EMAIL_DOMAIN}%' then preferred.email
                when lower(most_recent_active.email) like '%{_EMAIL_DOMAIN}%' then most_recent_active.email
                when preferred.email is not null then preferred.email
                when most_recent_active.email is not null then most_recent_active.email
                else lower(instructors."firstName"||instructors."lastName"||'@{_EMAIL_DOMAIN_WITH_EXT}')
            end                                     "email",
            instructors."firstName"                 "firstName",
            instructors."middleName"                "middleName",
            instructors."lastName"                  "lastName",
            'Teacher'                               "userRole",
			''                  					"sisUserId",					  -- conditional; required if "userRole" is "Student"
            ''                                      "includedInCourseFee",            -- conditional; Required if "userRole" is "Student"
            ''                                      "studentFullPartTimeStatus",      -- conditional; Required if "userRole" is "Student"
            ''                                      "creditHours"                     -- conditional; Required if "userRole" is "Student"
        from sfrstcr

        join ssbsect 
        on ssbsect.ssbsect_crn         = sfrstcr.sfrstcr_crn
        and ssbsect.ssbsect_term_code  = sfrstcr.sfrstcr_term_code

        left join stvdept on stvdept.stvdept_code   = ssbsect.ssbsect_subj_code

        join stvterm on stvterm.stvterm_code        = ssbsect.ssbsect_term_code

        JOIN (
            SELECT 
                spriden.spriden_pidm pidm,
                SPRIDEN.SPRIDEN_FIRST_NAME "firstName",
                SPRIDEN.SPRIDEN_MI "middleName",
                SPRIDEN.SPRIDEN_LAST_NAME "lastName",
                SIRASGN.SIRASGN_CRN crn,
                SIRASGN.SIRASGN_TERM_CODE term,
                SIRASGN.SIRASGN_VPDI_CODE vpdi
            FROM SPRIDEN
            INNER JOIN SIRASGN ON SPRIDEN.SPRIDEN_PIDM = SIRASGN.SIRASGN_PIDM
            WHERE SPRIDEN.SPRIDEN_CHANGE_IND IS NULL
        ) instructors 
        ON instructors.crn                  = SSBSECT.SSBSECT_CRN
        AND instructors.term                = SSBSECT.SSBSECT_TERM_CODE
        
        /* preferred email */
        left join (
            select 
                goremal.goremal_pidm pidm,
                goremal.goremal_email_address email
            from goremal 
            where goremal.goremal_preferred_ind = 'Y'
            and goremal.goremal_status_ind      = 'A'
        ) preferred
        on preferred.pidm                   = instructors.pidm
        
        /* most recent active email */
        left join (
            select 
                goremal.goremal_pidm pidm,
                goremal.goremal_email_address email
            from goremal 
            join (
                select
                    goremal.goremal_pidm pidm,
                    max(goremal.goremal_activity_date) md
                from goremal
                where goremal.goremal_status_ind = 'A' 
                group by
                    goremal.goremal_pidm
            ) maxd on maxd.pidm = goremal.goremal_pidm
                and maxd.md   = goremal.goremal_activity_date
            where goremal.goremal_status_ind    = 'A'
        ) most_recent_active on most_recent_active.pidm = instructors.pidm

        where sfrstcr.sfrstcr_rsts_code            in ('RE', 'RW')
        and {_TIME_FRAME}
    )
) main
where lower(main."lastName") not like '%do%not%use%'
  and lower(main."firstName") not like '%do%not%use%'
""".format(**locals())

_strSQLUsers = """
SELECT distinct
    ROW_NUMBER() OVER (
            ORDER BY main."firstName"
        ) 										            "recordNumber",
    main.*
from
(
    select distinct
        pop.jbln_code                                       "campus",
        ''                                                  "school",
        case
            when lower(preferred.email) like '%{_EMAIL_DOMAIN}%' then preferred.email
            when lower(most_recent_active.email) like '%{_EMAIL_DOMAIN}%' then most_recent_active.email
            when preferred.email is not null then preferred.email
            else most_recent_active.email
        end                                                 "email",
        case    
            WHEN aka.pidm IS NOT NULL THEN aka.FirstName
            ELSE spriden.SPRIDEN_FIRST_NAME
        END                                                 "firstName",
        CASE
            WHEN aka.pidm IS NOT NULL THEN aka.MiddleName
            ELSE spriden.SPRIDEN_MI
        END                                                 "middleName",
        CASE
            WHEN aka.pidm IS NOT NULL THEN aka.LastName
            ELSE spriden.SPRIDEN_LAST_NAME
        END                                                 "lastName",
        'administrator'                                     "userRole",
        ''                                                  "sisUserId"
    FROM spriden
    JOIN (
        SELECT 
            nbrjobs.nbrjobs_pidm pidm,
            MAX(nbrjobs.nbrjobs_jbln_code) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) jbln_code,
            MAX(nbrjobs.nbrjobs_effective_date) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) eff_date,
            MAX(nbrjobs.nbrjobs_desc) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) nbrjobs_desc,
            MAX(nbrbjob.nbrbjob_contract_type) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) ctype,
            MAX(nbrjobs.nbrjobs_orgn_code_ts) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) orgn_code,
            MAX(nbrjobs.nbrjobs_ecls_code) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) ecls_code,
            MAX(nbrjobs.nbrjobs_status) keep (dense_rank last
                ORDER BY nbrjobs.nbrjobs_effective_date) empl_status
        FROM nbrjobs
        JOIN nbrbjob ON nbrbjob.nbrbjob_pidm          = nbrjobs.nbrjobs_pidm
                    AND nbrbjob.nbrbjob_posn          = nbrjobs.nbrjobs_posn
                    AND nbrbjob.nbrbjob_suff          = nbrjobs.nbrjobs_suff
                    AND nbrjobs.nbrjobs_status       <> 'T'
                    AND nbrbjob.nbrbjob_contract_type = 'P'
        GROUP BY nbrjobs.nbrjobs_pidm
    ) pop ON pop.pidm = spriden.spriden_pidm
    JOIN (
        SELECT 
            pebempl.pebempl_pidm pidm,
            pebempl.pebempl_ecls_code ecls_code
        FROM pebempl
        WHERE pebempl.pebempl_empl_status <> 'T'
    ) emp_status ON emp_status.pidm = pop.pidm
    LEFT JOIN (
        SELECT DISTINCT 
            spriden.spriden_pidm pidm,
            spriden.spriden_last_name LastName,
            spriden.spriden_mi MiddleName,
            spriden.spriden_first_name FirstName
        FROM spriden
        WHERE spriden.spriden_ntyp_code = 'AKA'
    ) aka ON aka.pidm = spriden.spriden_pidm
    LEFT JOIN (
        SELECT 
            ftvorgn.ftvorgn_orgn_code orgn_code,
            ftvorgn.ftvorgn_title
        FROM ftvorgn
        JOIN (
            SELECT 
                ftvorgn.ftvorgn_orgn_code code,
                MAX(ftvorgn.ftvorgn_eff_date) md
            FROM ftvorgn
            GROUP BY ftvorgn.ftvorgn_orgn_code
        ) maxfd ON maxfd.code                    = ftvorgn.ftvorgn_orgn_code
               AND maxfd.md                     = ftvorgn.ftvorgn_eff_date
        WHERE ftvorgn.ftvorgn_status_ind = 'A'
    ) title ON title.orgn_code       = pop.orgn_code
    /* preferred email */
    left join (
        select 
            goremal.goremal_pidm pidm,
            goremal.goremal_email_address email
        from goremal 
        where goremal.goremal_preferred_ind = 'Y'
        and goremal.goremal_status_ind    = 'A'
    ) preferred on preferred.pidm               = pop.pidm
    /* most recent active email */
    left join (
        select 
            pidm,
            MAX(email) keep (dense_rank first order by preference) email
        from (
            select 
                goremal.goremal_pidm pidm,
                case
                    when lower(goremal.goremal_email_address) like '%{_EMAIL_DOMAIN}%' then 1
                    else 2
                end preference,
                goremal.goremal_email_address email
                from goremal 
                join (
                    select
                        goremal.goremal_pidm pidm,
                        max(goremal.goremal_activity_date) md
                    from goremal
                    where goremal.goremal_status_ind = 'A' 
                    group by
                        goremal.goremal_pidm
                ) maxd on maxd.pidm = goremal.goremal_pidm
                      and maxd.md   = goremal.goremal_activity_date
            where goremal.goremal_status_ind    = 'A'
        )
        group by pidm
    ) most_recent_active on most_recent_active.pidm               = pop.pidm
    WHERE spriden.spriden_change_ind  IS NULL
      AND
        CASE
            WHEN trim(BOTH ' '
                FROM (trim(BOTH '-'
                    FROM (SUBSTR(pop.nbrjobs_desc, 8))))) = 'STUDENT'
                THEN 'STUDENT WORKER'
            ELSE trim(BOTH ' '
                FROM (trim(BOTH '-'
                    FROM (SUBSTR(pop.nbrjobs_desc, 8)))))
        END                        <> 'STUDENT WORKER'
     AND emp_status.ECLS_CODE NOT IN ('CO', 'AC')
    and (
        (lower(pop.nbrjobs_desc) like '%dean%')
        or (lower(pop.nbrjobs_desc) like '%div%chair%')
        or (lower(pop.nbrjobs_desc) like '%chancellor%')
        or (lower(pop.nbrjobs_desc) like '%director%')
    )
) main
order by 1
"""

_listActiveQueries = [
    # ["{name.csv}", {query_string}, [list of columns]]
    ["courses.csv", _strSQLCourses, 
        ["recordNumber", "campus", "school", "institutionDepartment", "term", "department", "course", "section",                 
        "campusTitle", "schoolTitle", "institutionDepartmentTitle", "courseTitle", "institutionCourseCode", 
        "institutionClassCode", "institutionSubjectCodes", "institutionSubjectsTitle", "crn", "termTitle", 
        "termType", "termStartDate", "termEndDate", "sectionStartDate", "sectionEndDate", "classGroupId", 
        "estimatedEnrollment"
        ]
    ],
    ["enrollments.csv", _strSQLEnrollments, 
        ["recordNumber", "campus", "school", "institutionDepartment", "term", "department", "course", 
        "section", "email", "firstName", "middleName", "lastName", "userRole", "sisUserId",	"includedInCourseFee", 
        "studentFullPartTimeStatus", "creditHours"
        ]
    ],
    ["users.csv", _strSQLUsers, 
        ["recordNumber", "campus", "school", "email", "firstName", "middleName", "lastName", "userRole", "sisUserId"]
    ]
]  
