// Exact and hybrid girth-cycle counting, extracted verbatim from four_algorithms.cpp.
#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;using Clock=chrono::steady_clock;
struct G{
 int n,m,N;vector<vector<int>>a,out;vector<int>from,to,reversePosition;
 explicit G(const string&p){
  ifstream f(p);int E;if(!(f>>n>>m>>E))throw runtime_error("bad graph");
  N=n+m;a.resize(N);out.resize(N);
  for(int i=0,u,v;i<E;i++){
   if(!(f>>u>>v)||u<0||u>=n||v<0||v>=m)throw runtime_error("invalid graph");
   v+=n;int id=from.size();from.push_back(u);to.push_back(v);
   from.push_back(v);to.push_back(u);
   reversePosition.push_back(out[u].size());reversePosition.push_back(out[v].size());
   out[u].push_back(id);out[v].push_back(id+1);a[u].push_back(v);a[v].push_back(u);
  }
 }
};
struct ExactState{
 const G&gr;int g,k,root=0,epoch=0;ull occurrences=0,probes=0;
 vector<int>dist,mark,cnt,nodes,cur,nxt,meet;
 explicit ExactState(const G&gg,int girth):gr(gg),g(girth),k(girth/2),
  dist(gg.N,-1),mark(gg.N),cnt(gg.N){nodes.reserve(gg.N);cur.reserve(gg.N);nxt.reserve(gg.N);meet.reserve(gg.N);}
 void runRoot(){
  int s=root++;++epoch;nodes.clear();cur.clear();cur.push_back(s);
  nodes.push_back(s);dist[s]=0;
  for(int level=0;level<k-1;level++){
   nxt.clear();for(int u:cur)for(int v:gr.a[u]){
    ++probes;if(dist[v]<0){dist[v]=level+1;nodes.push_back(v);nxt.push_back(v);}
   }cur.swap(nxt);
  }
  meet.clear();
  for(int u:cur)for(int v:gr.a[u]){
   ++probes;
   if(dist[v]<0){
    if(mark[v]!=epoch){mark[v]=epoch;cnt[v]=0;meet.push_back(v);}
    ++cnt[v];
   }
  }
  for(int v:meet)occurrences+=ull(cnt[v])*(cnt[v]-1)/2;
  for(int u:nodes)dist[u]=-1;
 }
 void advance(ull budget){
  ull initial=probes;while(root<gr.n&&probes-initial<budget)runRoot();
 }
 bool done()const{return root==gr.n;}
 ull result()const{
  if(!done()||occurrences%k)throw runtime_error("incomplete exact count");
  return occurrences/k;
 }
};
ull exact(const G&g,int girth){ExactState s(g,girth);s.advance(ULLONG_MAX);return s.result();}
struct Sampler{
 const G&gr;int g,r,success=0,start=-1,v=-1,back=-1,depth=0;
 ull trials=0,probes=0;mt19937_64 rng;
 Sampler(const G&gg,int girth,int target,ull seed):
  gr(gg),g(girth),r(target),rng(seed){}
 void advance(ull credits){
  ull used=0;
  while(success<r&&used<credits){
   if(depth==0){start=uniform_int_distribution<int>(0,gr.n-1)(rng);v=start;back=-1;}
   int d=gr.out[v].size();
   int j=uniform_int_distribution<int>(0,d-1-(back>=0))(rng);
   if(back>=0&&j>=back)j++;
   int e=gr.out[v][j];v=gr.to[e];
   back=gr.reversePosition[e^1];depth++;used++;probes++;
   if(depth==g){trials++;success+=(v==start);depth=0;}
  }
 }
};
double Bvalue(const G&gr,int g){
 double dv=gr.a[0].size(),dc=gr.a[gr.n].size();
 return dv*pow(dv-1,g/2-1)*pow(dc-1,g/2);
}
struct HybridResult{double estimate;bool sampled;ull exactops,sampleops;};
HybridResult hybrid(const G&gr,int g,int r,ull seed){
 ExactState ex(gr,g);Sampler sp(gr,g,r,seed);
 double scale=gr.n*Bvalue(gr,g)/g;const ull quantum=8192;
 while(true){
  if(!ex.done())ex.advance(quantum);
  if(ex.done())return {double(ex.result()),false,ex.probes,sp.probes};
  if(sp.success<r)sp.advance(quantum);
  if(sp.success>=r)
   return {scale*(r-1)/double(sp.trials-1),true,ex.probes,sp.probes};
 }
}
