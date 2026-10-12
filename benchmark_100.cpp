// 100 randomized paired runs of unchanged Exact and Hybrid implementations.
#include "exact_hybrid.cpp"
static pair<double,double> stats(const vector<double>&v){
 double sum=accumulate(v.begin(),v.end(),0.0);
 double mu=sum/v.size(),sq=0;
 for(double a:v){double d=a-mu;sq+=d*d;}
 return {mu,sqrt(sq/(v.size()-1))};
}
int main(int argc,char**argv){
 try{
  if(argc<4)throw runtime_error("usage: benchmark_100 graph.edges girth expectedNg [reps]");
  G gr(argv[1]);int girth=stoi(argv[2]);ull expected=stoull(argv[3]);
  if(argc>4&&string(argv[4])=="verify"){if(exact(gr,girth)!=expected)throw runtime_error("Exact girth count mismatch");cout<<"VERIFIED "<<expected<<"\n";return 0;}
  int repeats=argc>4?stoi(argv[4]):100;
  if(repeats!=100)throw runtime_error("final protocol requires exactly 100 trials");
  vector<double> timings[2];for(auto &x:timings)x.reserve(repeats);
  mt19937_64 orderRng(26012027);
  double errorSum=0;int sampledWins=0;
  for(int trial=0;trial<repeats;trial++){
   array<int,2> order={0,1};
   shuffle(order.begin(),order.end(),orderRng);
   for(int alg:order){
    auto t0=Clock::now();
    if(alg==1){
     auto v=hybrid(gr,girth,100,20261012+1009*trial);
     double ms=chrono::duration<double,milli>(Clock::now()-t0).count();
     timings[alg].push_back(ms);
     if(!isfinite(v.estimate))throw runtime_error("nonfinite hybrid result");
     errorSum+=100.0*abs(v.estimate-double(expected))/double(expected);
     sampledWins+=v.sampled;
    }else{
     ull count=exact(gr,girth);
     double ms=chrono::duration<double,milli>(Clock::now()-t0).count();
     if(count!=expected)throw runtime_error("COUNT DISAGREES at trial "+to_string(trial)+", algorithm "+to_string(alg));
     timings[alg].push_back(ms);
    }
   }
  }
  cout<<fixed<<setprecision(9)
      <<"{\"n\":"<<gr.n<<",\"g\":"<<girth<<",\"Ng\":"<<expected
      <<",\"reps\":"<<repeats<<",\"random_wins\":"<<sampledWins
      <<",\"MARE_percent\":"<<errorSum/repeats;
  const char*keys[]={"Exact","Hybrid"};
  for(int a=0;a<2;a++){
   auto [mean,sd]=stats(timings[a]);
   auto sorted=timings[a];sort(sorted.begin(),sorted.end());
   cout<<",\""<<keys[a]<<"_ms\":"<<mean
       <<",\""<<keys[a]<<"_std_ms\":"<<sd
       <<",\""<<keys[a]<<"_median_ms\":"<<(sorted[49]+sorted[50])/2;
  }
  cout<<"}\n";
 }catch(exception&e){cerr<<"ERROR: "<<e.what()<<"\n";return 1;}
}
