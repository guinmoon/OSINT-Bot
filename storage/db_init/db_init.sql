--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2 (Debian 14.2-1.pgdg110+1)
-- Dumped by pg_dump version 14.0

-- Started on 2022-02-25 14:43:25 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 16390)
-- Name: phones; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.phones (
    id bigint NOT NULL,
    phone character varying(100)
);


ALTER TABLE public.phones OWNER TO guinmoon;

--
-- TOC entry 211 (class 1259 OID 16389)
-- Name: phones_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.phones ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.phones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 16396)
-- Name: phones_info_parsed; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.phones_info_parsed (
    id bigint NOT NULL,
    phone_id bigint NOT NULL,
    info character varying(500),
    info_type bigint,
    uid character varying(150)
);


ALTER TABLE public.phones_info_parsed OWNER TO guinmoon;

--
-- TOC entry 213 (class 1259 OID 16395)
-- Name: phones_info_parsed_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.phones_info_parsed ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.phones_info_parsed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 16386)
-- Name: ref_phone_info_types; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.ref_phone_info_types (
    id bigint NOT NULL,
    type character varying(100)
);


ALTER TABLE public.ref_phone_info_types OWNER TO guinmoon;

--
-- TOC entry 209 (class 1259 OID 16385)
-- Name: ref_phone_info_types_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.ref_phone_info_types ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ref_phone_info_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 218 (class 1259 OID 16443)
-- Name: telebot_log; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.telebot_log (
    id bigint NOT NULL,
    from_user_id bigint NOT NULL,
    from_user_nick character varying(100),
    from_user_name character varying(100),
    message character varying(500),
    date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.telebot_log OWNER TO guinmoon;

--
-- TOC entry 217 (class 1259 OID 16442)
-- Name: telebot_log_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.telebot_log ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.telebot_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 16457)
-- Name: telebot_log_responses; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.telebot_log_responses (
    id bigint NOT NULL,
    from_user_id bigint NOT NULL,
    from_user_nick character varying(100),
    from_user_name character varying(100),
    response_text text,
    message character varying(500),
    date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.telebot_log_responses OWNER TO guinmoon;

--
-- TOC entry 219 (class 1259 OID 16456)
-- Name: telebot_log_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.telebot_log_responses ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.telebot_log_responses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 16428)
-- Name: telebot_whitelist; Type: TABLE; Schema: public; Owner: guinmoon
--

CREATE TABLE public.telebot_whitelist (
    id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.telebot_whitelist OWNER TO guinmoon;

--
-- TOC entry 215 (class 1259 OID 16427)
-- Name: telebot_whitelist_id_seq; Type: SEQUENCE; Schema: public; Owner: guinmoon
--

ALTER TABLE public.telebot_whitelist ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.telebot_whitelist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3197 (class 2606 OID 16426)
-- Name: phones phone; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phone UNIQUE (phone);


--
-- TOC entry 3201 (class 2606 OID 16400)
-- Name: phones_info_parsed phones_info_parsed_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones_info_parsed
    ADD CONSTRAINT phones_info_parsed_pkey PRIMARY KEY (id);


--
-- TOC entry 3199 (class 2606 OID 16394)
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (id);


--
-- TOC entry 3195 (class 2606 OID 16411)
-- Name: ref_phone_info_types ref_phone_info_types_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.ref_phone_info_types
    ADD CONSTRAINT ref_phone_info_types_pkey PRIMARY KEY (id);


--
-- TOC entry 3207 (class 2606 OID 16447)
-- Name: telebot_log telebot_log_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.telebot_log
    ADD CONSTRAINT telebot_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3209 (class 2606 OID 16463)
-- Name: telebot_log_responses telebot_log_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.telebot_log_responses
    ADD CONSTRAINT telebot_log_responses_pkey PRIMARY KEY (id);


--
-- TOC entry 3205 (class 2606 OID 16432)
-- Name: telebot_whitelist telebot_whitelist_pkey; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.telebot_whitelist
    ADD CONSTRAINT telebot_whitelist_pkey PRIMARY KEY (id);


--
-- TOC entry 3203 (class 2606 OID 16418)
-- Name: phones_info_parsed uid_phone_type; Type: CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones_info_parsed
    ADD CONSTRAINT uid_phone_type UNIQUE (phone_id, uid, info_type);


--
-- TOC entry 3211 (class 2606 OID 16412)
-- Name: phones_info_parsed inf_type; Type: FK CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones_info_parsed
    ADD CONSTRAINT inf_type FOREIGN KEY (info_type) REFERENCES public.ref_phone_info_types(id) NOT VALID;


--
-- TOC entry 3210 (class 2606 OID 16401)
-- Name: phones_info_parsed phones; Type: FK CONSTRAINT; Schema: public; Owner: guinmoon
--

ALTER TABLE ONLY public.phones_info_parsed
    ADD CONSTRAINT phones FOREIGN KEY (phone_id) REFERENCES public.phones(id) NOT VALID;


-- Completed on 2022-02-25 14:43:27 MSK

--
-- PostgreSQL database dump complete
--

