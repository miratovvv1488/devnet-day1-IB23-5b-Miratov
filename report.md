# Day 1 Report — DevNet Sprint

## 1. Student
- Name: Miratov Mursalim
- Group: IB-23-5b
- GitHub repo: https://github.com/miratovvv1488/devnet-day1-IB23-5b-Miratov.git
- Day1 Token: D1-IB-23-5b-12-C19E

## 2. NetAcad progress (Module 1)
- Completed items: 1.1, 1.2, 1.3


## 3. VM evidence
- File: `artifacts/day1/env.txt` exists: Yes


## 4. Repo structure (must match assignment)
- `src/day1_api_hello.py` : Yes
- `tests/test_day1_api_hello.py` : Yes
- `schemas/day1_summary.schema.json` : Yes
- `artifacts/day1/summary.json` : Yes
- `artifacts/day1/response.json` : Yes

## 5. Commands run (paste EXACT output)
### 5.1 Script run
```text
{
  "schema_version": "1.0",
  "generated_utc": "2026-03-18T18:00:51.371041+00:00",
  "student": {
    "token": "D1-IB-23-5b-12-C19E",
    "name": "Miratov",
    "group": "IB-23-5b"
  },
  "api": {
    "url": "https://jsonplaceholder.typicode.com/todos/1",
    "status_code": 200,
    "validation_passed": true,
    "validation_errors": [],
    "response_sha256": "ffefdf50d54770c2a20ba143e42daa910535c20ec5ca7a1e449dac71729f00fe"
  },
  "run": {
    "python": "3.8.2",
    "platform": "linux"
  }
}
```
### 5.2 Tests
```text
1 passed in 0.17s
```

## 6. Что я изучил сегодня
- Как работать с Linux терминалом в DEVASC VM
- Как создавать и активировать Python virtual environment (venv)
- Как делать HTTP GET запрос через библиотеку requests
- Как сохранять JSON ответ и считать SHA256 хэш
- Как писать unit тесты с pytest и валидировать JSON по схеме
- Как работать с Git: создавать коммиты и пушить в GitHub

## 7. Проблемы и решения
- Problem: При запуске скрипта ошибка `ERROR: set STUDENT_TOKEN, STUDENT_NAME, STUDENT_GROUP`
- Fix: Переменные из `.env` не были загружены в сессию. Выполнил `export $(cat .env | xargs)`
- Proof: После экспорта скрипт отработал успешно, `validation_passed: true`