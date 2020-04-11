from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Item
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,ListView,CreateView, DeleteView, UpdateView
import hashlib
import time
import pickle
from django.views import View
from django.http import HttpResponseRedirect
class Block:

    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
                                              self.prev_hash, self.data,
                                              self.timestamp)

        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
                                               self.prev_hash, self.data,
                                               self.timestamp)


class BlockChain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    def construct_genesis(self):
        self.construct_block(proof_no=0, prev_hash=0)

    def construct_block(self, proof_no, prev_hash):
        block = Block(
            index=len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block

    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.prev_hash:
            return False

        elif not BlockChain.verifying_proof(block.proof_no,
                                            prev_block.proof_no):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, title, description, photo):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'title': title,
            'description': description,
            'photo': photo
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, details_miner):

        self.new_data(
            sender="0",  #it implies that this node has created a new block
            receiver=details_miner,
            title="first",  #creating a new block (or identifying the proof number) is awarded with 1
            description="first desc",
            phone=12345
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        #obtains block object from the block data

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])

def loadall(filename):
    with open(filename,'rb') as input:
        return pickle.load(input)
    for block in blockchain.chain:
        dt=block.data
        for a in dt:
            print(a['sender'])

# Create your views here.
def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home/home.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Item
    fields = ['status']

    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        post= self.get_object()
        if self.request.user.username=='naman':
            return True
        return False

class PostListView(ListView):
    model=Item
    template_name='home/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['-date_posted'] #Changes posts from oldest to newest fro viceversa remove - in front

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'desc', 'PhoneNo', "Address", "image"]

    def form_valid(self,form):
        form.instance.donor = self.request.user
        # blockchain = loadall('blck.pkl')
        # # blockchain=BlockChain()
        # # print(blockchain.chain)
        # for block in blockchain.chain:
        #     dt=block.data
        #     print(dt)

        # with open('blck.pkl','wb') as output:
        #     last_block = blockchain.latest_block
        #     last_proof_no = last_block.proof_no
        #     proof_no = blockchain.proof_of_work(last_proof_no)
        #     blockchain.new_data(
        #         sender = form.instance.donor.username,
        #         recipient = 'naman',
        #         title = form.instance.title,
        #         description = form.instance.desc,
        #         phone = form.instance.PhoneNo
        #     )
        #     last_hash = last_block.calculate_hash
        #     block = blockchain.construct_block(proof_no, last_hash)
        #     # print(blockchain.chain)
        #     pickle.dump(blockchain, output, pickle.HIGHEST_PROTOCOL)
        #     # print(form.instance.title)
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model=Item
    print(model.title)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Item
    success_url='/'
    def test_func(self):
        item=self.get_object()
        print("In the delte")
        if(self.request.user==item.donor or self.request.user.username=="naman"):
            return True
        return False

def approve(request, pk):
    item=Item.objects.get(pk=pk)
    item.status = 'approved'
    item.save()
    rec="naman"
    name=item.title
    if(request.user.username=="naman"):
        blockchain = loadall('blck.pkl')
        with open('blck.pkl','wb') as output:
            last_block = blockchain.latest_block
            last_proof_no = last_block.proof_no
            proof_no = blockchain.proof_of_work(last_proof_no)
            blockchain.new_data(
                sender = item.donor.username,
                recipient = rec,
                title = item.title,
                description = item.desc,
                # phone = item.PhoneNo
                photo = item.image
            )
            last_hash = last_block.calculate_hash
            block = blockchain.construct_block(proof_no, last_hash)
            print(blockchain.chain)
            pickle.dump(blockchain, output, pickle.HIGHEST_PROTOCOL)
    pri=str(pk)
    redirectpath="/post/"+pri+"/delete"
    return HttpResponseRedirect(redirectpath)
    
    
def deny(request, pk):
    item=Item.objects.get(pk=pk)
    item.status = 'rejected'
    item.save()
    name=item.title
    if(request.user.username=="naman"):
        blockchain = loadall('blck.pkl')
        with open('denyblck.pkl','wb') as output:
            last_block = blockchain.latest_block
            last_proof_no = last_block.proof_no
            proof_no = blockchain.proof_of_work(last_proof_no)
            blockchain.new_data(
                sender = item.donor.username,
                recipient = 'naman',
                title = item.title,
                description = item.desc,
                # phone = item.PhoneNo
                photo = item.image
            )
            last_hash = last_block.calculate_hash
            block = blockchain.construct_block(proof_no, last_hash)
            print(blockchain.chain)
            pickle.dump(blockchain, output, pickle.HIGHEST_PROTOCOL)
    pri=str(pk)
    redirectpath="/post/"+pri+"/delete"
    return HttpResponseRedirect(redirectpath)

def userDetail(request, username):
    blockchain=loadall('blck.pkl')
    denyblockchain=loadall('denyblck.pkl')
    count=0
    red=0
    for block in blockchain.chain:
        dt=block.data
        for i in dt:
            if(type(i['sender'])==str and i['sender']==username):
                count+=1
    for block in denyblockchain.chain:
        dt=block.data
        for i in dt:
            if(type(i['sender'])==str and i['sender']==username):
                red+=1
    count=count-red
    context={
        'username':username,
        'blockchain':blockchain,
        'denyblockchain':denyblockchain,
        'items': Item.objects.all(),
        'count':count
    }
    return render(request, 'home/userdetail.html', context)

def about(request):
    return render(request, 'home/about.html')

@login_required
def get_all_donations(request):
    blockchain=loadall('blck.pkl')
    context = {
        'blockchain': blockchain
    }
    return render(request, 'home/all_donations.html', context)

# class approve(View):
#     model=Item
#     def __init__(self, kwargs):
#         item=self.kwargs['pk']
#         print(item.title)
#         # return render(request, 'home/home.html')

# class approve():
#     model=Item
#     item=self.get_object()
#     blockchain = loadall('blck.pkl')
#         # blockchain=BlockChain()
#         # print(blockchain.chain)
#     for block in blockchain.chain:
#         dt=block.data
#         print(dt)
#     with open('blck.pkl','wb') as output:
#         last_block = blockchain.latest_block
#         last_proof_no = last_block.proof_no
#         proof_no = blockchain.proof_of_work(last_proof_no)
#         blockchain.new_data(
#             sender = item.donor,
#             recipient = 'naman',
#             title = item.title,
#             description = item.desc,
#             phone = item.PhoneNo
#         )
#         last_hash = last_block.calculate_hash
#         block = blockchain.construct_block(proof_no, last_hash)
#             # print(blockchain.chain)
#         pickle.dump(blockchain, output, pickle.HIGHEST_PROTOCOL)
#             # print(form.instance.title)
