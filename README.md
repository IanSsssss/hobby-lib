# hobby-lib
An AI-powered learning platform that creates personalized study plans for your interests

# data-model

## lesson-user
* email
* lessonName
* lessonContent
* process
* status
```
CREATE TABLE lesson_user (
    email VARCHAR(255) NOT NULL,
    lessonName VARCHAR(255) NOT NULL,
    lessonContent JSON NOT NULL,
    process JSON NOT NULL,
    finish BOOLEAN NOT NULL,
    lessonTime INTEGER NOT NULL,
    PRIMARY KEY (email, lessonName)
);
```
## exam