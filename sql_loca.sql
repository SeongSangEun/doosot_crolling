create table loca(
    loca_num number PRIMARY KEY,
    loca_name varchar2(50) unique,
    loca_addr varchar2(100),
    loca_phone varchar2(50),
    loca_img varchar2(100),
    loca_date date default sysdate,
    loca_valid varchar2(10)
);

-- 테이블 삭제
drop table loca purge;

-- 시퀀스 객체 생성
create sequence loca_num nocache nocycle;
