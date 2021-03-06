Search.setIndex({docnames:["application","index","library"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["application.rst","index.rst","library.rst"],objects:{"":{src:[0,0,0,"-"]},"src.lib":{aes:[2,0,0,"-"],cpa:[2,0,0,"-"],data:[2,0,0,"-"],traces:[2,0,0,"-"]},"src.lib.aes":{Handler:[2,1,1,""],Stages:[2,1,1,""],add_round_key:[2,4,1,""],block_to_words:[2,4,1,""],col_to_word:[2,4,1,""],inv_mix_columns:[2,4,1,""],inv_shift_rows:[2,4,1,""],inv_sub_bytes:[2,4,1,""],key_expansion:[2,4,1,""],mix_columns:[2,4,1,""],rot_word:[2,4,1,""],shift_rows:[2,4,1,""],sub_bytes:[2,4,1,""],sub_word:[2,4,1,""],word_to_col:[2,4,1,""],words_to_block:[2,4,1,""]},"src.lib.aes.Handler":{blocks:[2,2,1,""],decrypt:[2,3,1,""],encrypt:[2,3,1,""],keys:[2,2,1,""]},"src.lib.aes.Stages":{ADD_ROUND_KEY:[2,2,1,""],INV_ADD_ROUND_KEY:[2,2,1,""],INV_MIX_COLUMNS:[2,2,1,""],INV_SHIFT_ROWS:[2,2,1,""],INV_SUB_BYTES:[2,2,1,""],MIX_COLUMNS:[2,2,1,""],SHIFT_ROWS:[2,2,1,""],START:[2,2,1,""],SUB_BYTES:[2,2,1,""]},"src.lib.cpa":{Handler:[2,1,1,""],Statistics:[2,1,1,""]},"src.lib.cpa.Handler":{Models:[2,1,1,""],accumulate:[2,3,1,""],blocks:[2,2,1,""],clear:[2,3,1,""],correlations:[2,3,1,""],hypothesis:[2,2,1,""],key:[2,2,1,""],lens:[2,2,1,""],set_blocks:[2,3,1,""],set_key:[2,3,1,""],set_model:[2,3,1,""],sum2:[2,2,1,""],sum:[2,2,1,""],sums2:[2,2,1,""],sums:[2,2,1,""]},"src.lib.cpa.Handler.Models":{INV_SBOX_R10:[2,2,1,""],SBOX_R0:[2,2,1,""]},"src.lib.cpa.Statistics":{clear:[2,3,1,""],div_idxs:[2,3,1,""],graph:[2,3,1,""],guess_envelope:[2,3,1,""],guess_stats:[2,3,1,""],update:[2,3,1,""]},"src.lib.data":{Channel:[2,1,1,""],Deserializable:[2,1,1,""],Keywords:[2,1,1,""],Leak:[2,1,1,""],Meta:[2,1,1,""],Parser:[2,1,1,""],Request:[2,1,1,""],Serializable:[2,1,1,""]},"src.lib.data.Channel":{STR_MAX_LINES:[2,2,1,""],append:[2,3,1,""],ciphers:[2,2,1,""],clear:[2,3,1,""],insert:[2,3,1,""],keys:[2,2,1,""],plains:[2,2,1,""],pop:[2,3,1,""],read_csv:[2,3,1,""],write_csv:[2,3,1,""]},"src.lib.data.Deserializable":{read_csv:[2,3,1,""]},"src.lib.data.Keywords":{CIPHER:[2,2,1,""],CODE:[2,2,1,""],DELIMITER:[2,2,1,""],DIRECTION:[2,2,1,""],END_ACQ_TAG:[2,2,1,""],END_LINE_TAG:[2,2,1,""],ITERATIONS:[2,2,1,""],KEY:[2,2,1,""],MODE:[2,2,1,""],OFFSET:[2,2,1,""],PLAIN:[2,2,1,""],SAMPLES:[2,2,1,""],SENSORS:[2,2,1,""],START_RAW_TAG:[2,2,1,""],START_TRACE_TAG:[2,2,1,""],TARGET:[2,2,1,""],WEIGHTS:[2,2,1,""],all:[2,3,1,""],datawords:[2,2,1,""],idx:[2,2,1,""],inv:[2,2,1,""],meta:[2,2,1,""],metawords:[2,2,1,""],reset:[2,3,1,""],value:[2,2,1,""]},"src.lib.data.Leak":{STR_MAX_LINES:[2,2,1,""],append:[2,3,1,""],clear:[2,3,1,""],insert:[2,3,1,""],pop:[2,3,1,""],read_csv:[2,3,1,""],samples:[2,2,1,""],traces:[2,2,1,""],write_csv:[2,3,1,""]},"src.lib.data.Meta":{clear:[2,3,1,""],read_csv:[2,3,1,""],write_csv:[2,3,1,""]},"src.lib.data.Parser":{channel:[2,2,1,""],clear:[2,3,1,""],leak:[2,2,1,""],meta:[2,2,1,""],parse:[2,3,1,""],pop:[2,3,1,""]},"src.lib.data.Request":{ACQ_CMD_NAME:[2,2,1,""],Algos:[2,1,1,""],Directions:[2,1,1,""],Modes:[2,1,1,""],chunks:[2,2,1,""],command:[2,3,1,""],direction:[2,2,1,""],filename:[2,3,1,""],iterations:[2,2,1,""],mode:[2,2,1,""],requested:[2,3,1,""],source:[2,2,1,""],target:[2,2,1,""],total:[2,3,1,""],verbose:[2,2,1,""]},"src.lib.data.Request.Algos":{AES:[2,2,1,""],CRYPTON:[2,2,1,""],KLEIN:[2,2,1,""],PRESENT:[2,2,1,""]},"src.lib.data.Request.Directions":{DECRYPT:[2,2,1,""],ENCRYPT:[2,2,1,""]},"src.lib.data.Request.Modes":{CRYPTON:[2,2,1,""],DHUERTAS:[2,2,1,""],HARDWARE:[2,2,1,""],KLEIN:[2,2,1,""],OPENSSL:[2,2,1,""],PRESENT:[2,2,1,""],TINY:[2,2,1,""]},"src.lib.data.Serializable":{write_csv:[2,3,1,""]},"src.lib.traces":{Statistics:[2,1,1,""],adjust:[2,4,1,""],crop:[2,4,1,""],pad:[2,4,1,""],sync:[2,4,1,""]},"src.lib.traces.Statistics":{clear:[2,3,1,""],update:[2,3,1,""]},src:{lib:[2,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function"},terms:{"1024":1,"128":2,"2020":1,"4x4":2,"abstract":2,"byte":2,"class":2,"default":2,"enum":2,"export":[1,2],"function":2,"import":[1,2],"int":2,"new":2,"return":2,"true":2,AES:[1,2],The:[1,2],abc:2,about:[1,2],acceler:2,accord:[1,2],accumul:2,acq_cmd_nam:2,acquir:2,acquisit:[1,2],add_round_kei:2,addit:2,adjac:2,adjust:2,advanc:1,aes:1,after:2,again:2,agnost:2,aim:1,algo:2,algorithm:[1,2],all:[1,2],allow:2,alreadi:2,also:[1,2],altern:1,alwai:2,amount:2,analysi:1,ani:1,api:[1,2],app:1,appear:2,append:2,appli:2,arg:2,argument:[1,2],ark:2,arrai:2,ascii:2,attack:2,attribut:2,autodoc:1,autom:[1,2],avail:1,averag:2,avoid:2,backward:2,base:[1,2],basic:2,been:2,befor:2,begin:2,behavior:2,bench:1,best:2,between:2,binari:2,bit:2,bitwis:2,block:2,block_to_word:2,bool:2,both:2,brows:2,build:2,calibr:2,came:2,can:[1,2],cannot:2,caus:2,channel:[1,2],characterist:2,cheap:1,chunk:[1,2],cipher:2,classmethod:2,clear:2,clone:1,code:2,coeffici:2,col:2,col_to_word:2,collect:2,column:2,com:1,combin:2,command:2,commun:1,compar:2,complet:[1,2],comput:[1,2],consist:2,consumpt:2,contain:[1,2],content:1,convers:2,copyright:1,cor:2,cor_max:2,cor_min:2,core:1,correl:[1,2],correspond:2,count:2,cpa:1,creat:[1,2],crop:2,crypto:[1,2],crypton:2,csv:2,current:2,curv:2,dahoux:1,data:[1,2],dataword:2,dec:2,decrypt:2,delimit:2,deseri:1,deserializ:2,design:2,dev:1,develop:1,deviat:2,dhuerta:2,differ:2,difficult:1,direct:2,displai:2,div_idx:2,doc:1,doe:2,dtype:2,durat:2,dure:2,each:[1,2],eas:2,easili:2,effici:1,either:2,embed:1,empti:2,ems:1,enc:2,encapsul:2,encod:2,encourag:1,encrypt:[1,2],end:2,end_acq_tag:2,end_line_tag:2,entiti:2,enumer:2,envelop:2,equal:2,error:2,especi:2,exact:2,exampl:[1,2],exhaust:1,exist:2,expans:2,expect:2,eye:2,fals:2,fast:[1,2],featur:2,feel:1,file:2,filenam:2,fill:2,filter:2,follow:2,form:2,format:2,forward:2,free:1,from:[1,2],full:2,gather:1,gener:1,get:1,git:1,github:1,given:2,goal:1,graph:2,greater:2,greatli:1,guarante:2,guess:[1,2],guess_envelop:2,guess_stat:2,gui:1,handl:2,handler:2,hardwar:2,has:2,have:2,here:1,heterogen:1,hexadecim:2,high:2,host:1,howev:1,html:1,http:1,human:2,hypothesi:[1,2],idx:2,imag:1,implement:2,improv:1,independ:1,index:2,indexerror:2,infer:2,inferior:2,info:2,initi:2,input:2,insert:2,insid:1,instant:2,instruct:1,integ:2,intend:1,interfac:2,intermedi:2,inv:2,inv_add_round_kei:2,inv_mix_column:2,inv_sbox_r10:2,inv_shift_row:2,inv_sub_byt:2,invers:2,invovl:1,item:2,iter:[1,2],its:2,keep:2,kei:[1,2],key_expans:2,keyword:2,kind:1,klein:2,know:1,last:2,later:2,latter:1,leak:2,leakag:[1,2],least:1,len:2,length:2,level:2,lib:1,librari:2,line:2,list:[1,2],log:1,longest:2,look:1,mai:2,main:1,mainli:2,maintain:1,major:2,make:1,match:2,matric:2,matrix:2,max:2,maxim:2,maximum:2,mean:2,memori:2,messag:2,meta:2,metaword:2,method:2,might:1,min:2,minimum:2,mit:1,mix:2,mix_column:2,mode:2,model:[1,2],modul:1,more:2,must:[1,2],mutablesequ:2,name:2,ndarrai:2,need:2,next:2,nois:2,none:2,number:[1,2],numpi:2,object:2,occur:2,offset:2,onc:2,one:2,ones:2,open:1,openssl:2,oper:2,option:2,order:[1,2],our:1,out:2,over:2,own:[1,2],pad:2,paramet:2,parametr:1,pars:2,parser:2,part:1,pass:1,path:2,peak:2,pearson:2,per:2,perform:[1,2],pip3:1,pip:1,pipelin:2,plain:2,platform:1,pleas:1,plot:2,pop:2,port:[1,2],posit:2,power:2,precis:2,prefix:2,present:2,process:[1,2],programmat:2,project:1,properti:2,provid:[1,2],python3:1,python:[1,2],qualiti:1,quit:1,rais:2,rang:2,rank:2,read:2,read_csv:2,readabl:2,reason:2,recurr:2,reduc:1,refer:2,relat:2,remot:1,remov:2,report:2,repositori:1,repres:2,request:2,requir:1,reset:2,respect:2,result:[1,2],retriev:[1,2],revers:2,roll:2,rot_word:2,rotat:2,round:2,row:2,run:[1,2],same:2,sami:1,sampl:2,sas:1,sbox:2,sbox_r0:2,sca:[1,2],script:[1,2],search:2,segfault:2,self:2,sensor:2,separ:2,sequenc:2,serial:[1,2],serializ:2,set:2,set_block:2,set_kei:2,set_model:2,shell:1,shift:2,shift_row:2,shortest:2,side:[1,2],signal:[1,2],signific:1,simpl:2,sinc:1,size:[1,2],soc:2,softwar:1,sort:2,sourc:[1,2],specifi:2,sphinx:1,split:2,src:2,ssl:2,stack:1,stage:2,standard:[1,2],start:[1,2],start_raw_tag:2,start_trace_tag:2,stat:2,state:2,statist:[1,2],step:2,stop:2,store:2,str:2,str_max_lin:2,string:2,sub_byt:2,sub_word:2,sudo:1,suffix:2,sum2:2,sum:2,sums2:2,support:2,sync:2,synchron:2,system:1,take:1,target:[1,2],task:2,team:1,technic:1,tempor:2,term:2,test:1,than:2,thei:2,them:2,theses:2,thi:[1,2],threat:1,three:2,time:2,tini:2,tkinter:1,todai:1,togeth:2,tool:1,topic:1,total:2,trace:1,transform:2,truncat:2,ttyusb1:1,tutori:1,two:2,txt:1,type:2,uint8:2,under:1,unlik:2,until:2,updat:2,use:1,used:2,useful:2,using:[1,2],usual:2,valu:2,valueerror:2,vari:1,vast:1,venv:1,verbos:2,veri:1,via:2,view:1,visit:1,visual:1,want:2,warn:2,websit:1,weight:2,when:2,which:[1,2],wiki:1,without:2,word:2,word_to_col:2,words_to_block:2,work:1,wrap:2,write:2,write_csv:2,wrong:2,xfd:2,xfe:2,xff:2,xor:2,you:[1,2],your:[1,2]},titles:["Overview","Welcome to the SCABox documentation !","Overview"],titleterms:{aes:2,applic:1,attack:1,build:1,compat:1,contribut:1,cpa:2,demo:1,document:1,featur:1,instal:1,lib:2,librari:1,licens:1,log:2,main:0,modul:2,more:1,overview:[0,1,2],refer:1,scabox:1,trace:2,usag:1,welcom:1}})