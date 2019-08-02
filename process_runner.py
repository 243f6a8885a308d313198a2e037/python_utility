import sys
import subprocess


class SubprocessError(Exception):
    def __init__(self, completed_process):
        self.completed_process = completed_process


class SubprocessTimeoutError(Exception):
    def __init__(self, completed_process):
        self.completed_process = completed_process


class ProcessRunner:
    def __init__(self, name, command, timeout=1):
        self.name = name
        self.command = command
        self.timeout = timeout

    def run_with_timeout(self, cmdargs, timeout=None, input_=None, cwd=None, env=None, rusage=False):
        keyword_dic = {}
        if cwd:
            keyword_dic['cwd'] = cwd
        if env:
            keyword_dic['env'] = env
        keyword_dic['encoding'] = sys.stdout.encoding
        timeout = timeout if timeout else self.timeout
        timeout_cmd = 'time2out' if rusage else 'timeout'
        try:
            command = f'{timeout_cmd} --signal=KILL --kill-after={timeout + 1} {timeout} {self.command(cmdargs)}'
            result = subprocess.run(command, input=input_,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, **keyword_dic)
        except Exception as e:
            raise e
        if result.returncode == 128 + 9:
            # SIGKILL (almost certainly by timeout)
            raise SubprocessTimeoutError(result)
        if result.returncode != 0:
            raise SubprocessError(result)
        return result
