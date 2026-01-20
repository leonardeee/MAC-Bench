class Judge:
    def evaluate(self, judge_log: str, exit_code: int) -> dict:
        status = "pass" if exit_code == 0 else "violation"
        return {"status": status, "log": judge_log.strip()}
