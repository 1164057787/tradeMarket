
class MsgResponse():
    def __init__(self):
        self.status=100
        self.msg="success"
    @property
    def get_dict(self):
        return self.__dict__

if __name__== '__main__':
    res=MsgResponse()
    res.status=402
    res.msg='失败'
    # res.data={'name':"jjj"}
    print(res.get_dict)
