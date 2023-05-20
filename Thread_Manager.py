import threading
from Log_Manager import *


class THREAD_PRESET(threading.Thread):
    def __init__(self, target, args=() , daemon=False):
        super(THREAD_PRESET, self).__init__()
        self.target = target
        self.args = args
        self.daemon= daemon
        self.result = None

    def run(self):
        self.result = self.target(*self.args)

class Thread_DataManager:
    def __init__(self) -> None:
        self.USERS=[]
        self.SESSIONS={}
        self.USERS_COUNT=0
        self.user_socket_dict={}

class Thread:
    def __init__(self):
        self.ACTIVATED_THREADS={}
        self.USERS=Thread_DataManager().USERS
        self.SESSIONS=Thread_DataManager().SESSIONS
        self.USERS_COUNT=Thread_DataManager().USERS_COUNT
        self.THREADS_COUNT=0
        self.user_socket_dict={}
        self.stopped_threads={}
        self.finished_users=[]
        self.log=Log().logging

    def display_variables(self):
        LIST_VARIABLES=f'''
                            'SESSIONS':{self.SESSIONS},
                            'USERS':{self.USERS},
                            'USERS_COUNT':{self.USERS_COUNT},
                            'ACTIVATED_THREADS':{self.ACTIVATED_THREADS},
                            'THREADS_COUNT':{self.THREADS_COUNT}
                            'user_thread_result_dict':{self.user_thread_result_dict}
                            'user_socket_dict':{self.user_socket_dict}
                            'stopped_threads':{self.stopped_threads}
                            'finished_users':{self.finished_users}
                        '''
        print(LIST_VARIABLES)

    def Create_Thread(self, target, args=(), daemon=False):
        thread_mutex=0
        while True:
            new_thread_name='THREAD_{}_{}'.format(target.__name__,thread_mutex)
            self.THREADS_COUNT+=1
            if new_thread_name not in self.ACTIVATED_THREADS.keys():
                globals()[new_thread_name] = THREAD_PRESET(target=target,args=args,daemon=daemon)
                new_thread=globals()[new_thread_name]
                self.ACTIVATED_THREADS[new_thread_name]=new_thread
                return new_thread_name,new_thread
            else:
                thread_mutex+=1

    def clearSessionInfo(self,thread_name,user):
        thread=eval(thread_name)
        if (thread.is_alive()==False):
            del self.user_socket_dict[user]
            del self.finished_users[self.finished_users.index(user)]
            del self.USERS[self.USERS.index(user)]
            del self.SESSIONS[thread_name]
            self.USERS_COUNT-=1
        self.THREADS_COUNT-=1

    def find_stopped_thread(self):
        for activated_thread_name,thread in self.ACTIVATED_THREADS.copy().items():
            if 'stopped' in str(thread) :
                del self.ACTIVATED_THREADS[activated_thread_name]
                self.stopped_threads[activated_thread_name]=thread