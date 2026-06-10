-- ============================================================
-- LMS Database Creation Script for SQL Server (SSMS)
-- Equivalent to SQLAlchemy models in backend/app/models.py
-- ============================================================

USE master;
GO

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'lms_db')
BEGIN
    CREATE DATABASE lms_db
        COLLATE Cyrillic_General_CI_AS;
END
GO

USE lms_db;
GO

-- ============================================================
-- TABLE: users
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    CREATE TABLE users (
        id            NVARCHAR(36)  NOT NULL
                          CONSTRAINT PK_users PRIMARY KEY
                          CONSTRAINT DF_users_id DEFAULT (LOWER(NEWID())),
        email         NVARCHAR(255) NOT NULL
                          CONSTRAINT UQ_users_email UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        role          NVARCHAR(20)  NOT NULL
                          CONSTRAINT DF_users_role   DEFAULT 'STUDENT'
                          CONSTRAINT CK_users_role   CHECK (role IN ('STUDENT', 'INSTRUCTOR', 'ADMIN')),
        created_at    DATETIME2     NOT NULL
                          CONSTRAINT DF_users_created_at DEFAULT SYSUTCDATETIME()
    );

    CREATE INDEX IX_users_email ON users (email);
END
GO

-- ============================================================
-- TABLE: courses
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'courses')
BEGIN
    CREATE TABLE courses (
        id          NVARCHAR(36)   NOT NULL
                        CONSTRAINT PK_courses PRIMARY KEY
                        CONSTRAINT DF_courses_id DEFAULT (LOWER(NEWID())),
        title       NVARCHAR(500)  NOT NULL,
        description NVARCHAR(MAX)  NOT NULL CONSTRAINT DF_courses_description DEFAULT '',
        instructor  NVARCHAR(255)  NOT NULL CONSTRAINT DF_courses_instructor  DEFAULT '',
        image       NVARCHAR(1000) NOT NULL CONSTRAINT DF_courses_image       DEFAULT '',
        category    NVARCHAR(50)   NOT NULL
                        CONSTRAINT DF_courses_category DEFAULT 'OTHER'
                        CONSTRAINT CK_courses_category CHECK (
                            category IN ('PROGRAMMING','DESIGN','MARKETING',
                                         'BUSINESS','LANGUAGES','OTHER')
                        ),
        created_at  DATETIME2      NOT NULL CONSTRAINT DF_courses_created_at  DEFAULT SYSUTCDATETIME(),
        updated_at  DATETIME2      NOT NULL CONSTRAINT DF_courses_updated_at  DEFAULT SYSUTCDATETIME()
    );

    CREATE INDEX IX_courses_title ON courses (title);
END
GO

-- ============================================================
-- TABLE: lessons
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'lessons')
BEGIN
    CREATE TABLE lessons (
        id          NVARCHAR(36)  NOT NULL
                        CONSTRAINT PK_lessons PRIMARY KEY
                        CONSTRAINT DF_lessons_id DEFAULT (LOWER(NEWID())),
        course_id   NVARCHAR(36)  NOT NULL
                        CONSTRAINT FK_lessons_course FOREIGN KEY REFERENCES courses (id)
                            ON DELETE CASCADE ON UPDATE CASCADE,
        title       NVARCHAR(500) NOT NULL,
        lesson_type NVARCHAR(20)  NOT NULL
                        CONSTRAINT DF_lessons_lesson_type DEFAULT 'TEXT'
                        CONSTRAINT CK_lessons_lesson_type CHECK (lesson_type IN ('TEXT', 'VIDEO')),
        content     NVARCHAR(MAX) NOT NULL CONSTRAINT DF_lessons_content      DEFAULT '{}',
        order_index INT           NOT NULL CONSTRAINT DF_lessons_order_index  DEFAULT 0
    );
END
GO

-- ============================================================
-- TABLE: quizzes
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'quizzes')
BEGIN
    CREATE TABLE quizzes (
        id             NVARCHAR(36)  NOT NULL
                           CONSTRAINT PK_quizzes PRIMARY KEY
                           CONSTRAINT DF_quizzes_id DEFAULT (LOWER(NEWID())),
        lesson_id      NVARCHAR(36)  NOT NULL
                           CONSTRAINT FK_quizzes_lesson FOREIGN KEY REFERENCES lessons (id)
                               ON DELETE CASCADE ON UPDATE CASCADE,
        title          NVARCHAR(500) NOT NULL,
        time_limit_sec INT           NOT NULL CONSTRAINT DF_quizzes_time_limit_sec DEFAULT 600,
        passing_score  FLOAT         NOT NULL CONSTRAINT DF_quizzes_passing_score  DEFAULT 0.7,
        creator_id     NVARCHAR(36)  NULL
                           CONSTRAINT FK_quizzes_creator FOREIGN KEY REFERENCES users (id)
                               ON DELETE SET NULL ON UPDATE CASCADE,

        -- enforce one quiz per lesson (same as uselist=False in SQLAlchemy)
        CONSTRAINT UQ_quizzes_lesson_id UNIQUE (lesson_id)
    );
END
GO

-- ============================================================
-- TABLE: questions
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'questions')
BEGIN
    CREATE TABLE questions (
        id             NVARCHAR(36)  NOT NULL
                           CONSTRAINT PK_questions PRIMARY KEY
                           CONSTRAINT DF_questions_id DEFAULT (LOWER(NEWID())),
        quiz_id        NVARCHAR(36)  NOT NULL
                           CONSTRAINT FK_questions_quiz FOREIGN KEY REFERENCES quizzes (id)
                               ON DELETE CASCADE ON UPDATE CASCADE,
        type           NVARCHAR(30)  NOT NULL
                           CONSTRAINT CK_questions_type CHECK (
                               type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'TRUE_FALSE')
                           ),
        text           NVARCHAR(MAX) NOT NULL,
        options        NVARCHAR(MAX) NOT NULL CONSTRAINT DF_questions_options        DEFAULT '[]',
        correct_answer NVARCHAR(MAX) NOT NULL CONSTRAINT DF_questions_correct_answer DEFAULT '{}'
    );
END
GO

-- ============================================================
-- TABLE: attempts
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'attempts')
BEGIN
    CREATE TABLE attempts (
        id          NVARCHAR(36) NOT NULL
                        CONSTRAINT PK_attempts PRIMARY KEY
                        CONSTRAINT DF_attempts_id DEFAULT (LOWER(NEWID())),
        user_id     NVARCHAR(36) NOT NULL
                        CONSTRAINT FK_attempts_user FOREIGN KEY REFERENCES users (id),
        quiz_id     NVARCHAR(36) NOT NULL
                        CONSTRAINT FK_attempts_quiz FOREIGN KEY REFERENCES quizzes (id),
        status      NVARCHAR(20) NOT NULL
                        CONSTRAINT DF_attempts_status DEFAULT 'IN_PROGRESS'
                        CONSTRAINT CK_attempts_status CHECK (
                            status IN ('IN_PROGRESS', 'COMPLETED', 'AUTO_GRADED')
                        ),
        score       FLOAT        NULL,
        started_at  DATETIME2    NOT NULL CONSTRAINT DF_attempts_started_at  DEFAULT SYSUTCDATETIME(),
        finished_at DATETIME2    NULL
    );
END
GO

-- ============================================================
-- Verification: list created tables
-- ============================================================
SELECT
    t.name                    AS table_name,
    COUNT(c.column_id)        AS column_count
FROM sys.tables  t
JOIN sys.columns c ON c.object_id = t.object_id
WHERE t.type = 'U'
GROUP BY t.name
ORDER BY t.name;
GO
