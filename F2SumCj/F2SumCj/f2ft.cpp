
using namespace std;

#include <ilcplex/ilocplex.h>

ILOSTLBEGIN

#include <iostream>
#include <vector>
#include <list>
#include <algorithm>
#include <windows.h>

#define MAX_JOBS 600


double sp_time;
double avg_sp_time = 0;
double max_sp_time = 0;

int initial_obj;
int init_FO;

int sp_cnt = 0;
int r = -1;
int  h = -1;

struct Job {
	int id;
	int ptime[2];
};

vector<int> get_sequence(IloCplex cpx, IloIntVarArray x[], const vector<Job>& N, vector<int>& S)
{
	for (int i = 0; i < N.size(); ++i) {
		for (int j = 0; j < N.size(); ++j) {
			if (cpx.getValue(x[i][j]) > .5) {
				S[j] = N[i].id;
			}
		}
	}
	return S;
}

vector<vector<int>> get_S_with_ptime(const vector<Job>& N, vector<int>& S) {
	//Sprime.clear()
	vector<vector<int>> Sptime(N.size(), vector<int>(2, 0));
	for (int j = 0; j < N.size(); ++j) {
		Sptime[j][0] = N[S[j]].ptime[0];
		Sptime[j][1] = N[S[j]].ptime[1];
	}
	return Sptime;
}

float calculateI(float baseFO, float targetFO) {
	float improvement = 1 - (targetFO / baseFO);
	return improvement;
}

string printVec(vector<vector<int>> vect) {
	vector<int> temp_vect(vect.size());
	stringstream s;
	s << "\"[";
	for (vector<vector<int>>::iterator ite = vect.begin(); ite != vect.end(); ite++)
	{
		temp_vect = *ite;
		s << "[" << temp_vect[0] << "," << temp_vect[1] << "],";
	}
	s << "]\"";
	string ss = s.str();
	return ss;
}

void writeCSV(vector<vector<int>>& S, vector<vector<int>>& Sprime, int r, int h, float I, float Iprime, string csv) {
	std::ofstream myfile;
	myfile.open(csv, ios::app);
	string ss = printVec(S);
	string ssp = printVec(Sprime);
	myfile << ss << "," << ssp << "," << r << "," << h << "," << I << "," << Iprime << "\n";
	myfile.close();
}


bool
search(IloCplex cpx, IloIntVarArray x[], vector<Job>& N, vector<int>& S, float&bestobj, double timelim = 1e20)
{
	int iter = 0;
	vector<vector<int>> S_origin(N.size(), vector<int>(2, 0));
	vector<vector<int>> S_prime(N.size(), vector<int>(2, 0));

	while (iter < 15)
	{
		float rbs_FO = bestobj;
		cout << "rbs_FO: " << rbs_FO<<"\n";

		S_origin = get_S_with_ptime(N, S);
	
		cout << "initial=" << bestobj << endl;

		clock_t start_time = clock();

		for (int j = 6; j < 18 && j < N.size(); j++) {
			int max_Nr_win = N.size() - j;
			for (int s = 0; s < max_Nr_win; s++) {
				list<pair<int, int> > L;

				for (int i = 0; i < N.size(); i++) {
					if (i < s || i > s + j - 1) {
						x[S[i]][i].setLB(1);
						x[S[i]][i].setUB(1);
						L.push_back(pair<int, int>(S[i], i));
					}
				}

				clock_t sp_start = clock();
				cpx.solve();
				sp_time = ((double)(clock() - sp_start) / CLOCKS_PER_SEC);
				avg_sp_time += sp_time;
				sp_cnt++;
				if (sp_time > max_sp_time) {
					max_sp_time = sp_time;
				} 

				if ((float)cpx.getObjValue() < (bestobj-0.000001)) {
					bestobj = cpx.getObjValue();
					cout << "bestobj:--------" << bestobj<<endl;
					get_sequence(cpx, x, N, S);
					cout << "iteration:------" << iter << endl;
					cout << "r :" << s << "\t" << "h: " << j << endl;
					S_prime = get_S_with_ptime(N, S);
					cout << "Improved to " << bestobj <<
						" at time " << ((double)(clock() - start_time)) / CLOCKS_PER_SEC << endl;
					r = s;
					h = j;
				}
				while (!L.empty()) {
					x[L.front().first][L.front().second].setLB(0);
					x[L.front().first][L.front().second].setUB(1);
					L.pop_front();
				}
			}			
		}
		
		if (abs(rbs_FO - bestobj)<0.001) {
			return 0;
		}else{
			cout << "------------------------------------------------------------" << "\n";
			cout << "r :" << r << "\t" << "h: " << h << endl;
			cout << "iteration:----------" << iter << endl;
			//vector<int> Sprime = get_sequence(cpx, x, N, S);
			//for (vector<int>::iterator ite = Sprime.begin(); ite != Sprime.end(); ite++)
			//	cout << *ite << " ";
			cout << "BestObj:------------------------" << bestobj << "\n";
			cout << "init_FO:--------------------" << init_FO << "\n";
			cout << "rbs_FO:----------------------" << rbs_FO << "\n";
			cout << "------------------------------------------------------------" << "\n";

			float I = calculateI(float(init_FO), float(rbs_FO));
			float Iprime = calculateI(float(init_FO), float(bestobj));
			writeCSV(S_origin, S_prime, r, h, I, Iprime, "base.csv");
		}
		iter ++;
	}
	std::ofstream myfile;
	myfile.open("base.csv", ios::app);
	myfile << "\n";
}

//bool
//search(IloCplex cpx, IloIntVarArray x[], vector<Job>& N, vector<int>& S, int&bestobj, double timelim)
//{
//	int iter = 0;
//	
//	vector<vector<int>> S_origin(N.size(), vector<int>(2, 0));
//	vector<vector<int>> S_prime(N.size(), vector<int>(2, 0));
//	while (iter < 15)
//	{
//		int rbs_FO = bestobj;
//		cout << "rbs_FO----------------: " << rbs_FO<<"\n";
//
//		
//
//		S_origin = get_S_with_ptime(N, S);
//		cout << "initial=" << bestobj << endl;
//		int n = 0;
//		clock_t start_time = clock();                                                                                                                                                                                                                                                                
//		int count = 0;                                                 
//		for (int j = 6; j < 18 && j < N.size(); j++) {
//			int max_Nr_win = N.size() - j;
//			for (int s = 0; s < max_Nr_win; s++) {				
//				list<pair<int, int> > L;
//				for (int i = 0; i < N.size(); i++) {
//					if (i < s || i > s + j - 1) {
//						x[S[i]][i].setLB(1);
//						x[S[i]][i].setUB(1);
//						L.push_back(pair<int, int>(S[i], i));
//					}
//				} 
//
//				clock_t sp_start = clock();
//				cpx.solve();
//				count ++;
//				cout << "times of cplex:" <<count<<"\t";
//				sp_time = ((double)(clock() - sp_start) / CLOCKS_PER_SEC);
//				avg_sp_time += sp_time;
//				sp_cnt++;
//				if (sp_time > max_sp_time) {
//					max_sp_time = sp_time;
//				}
//
//				if (cpx.getObjValue() < bestobj) {
//					bestobj = cpx.getObjValue();
//					cout << "r :" << s << "\t" << "h: " << j << endl;
//					vector<int> Sprime = get_sequence(cpx, x, N, S);
//					S_prime = get_S_with_ptime(N, S);
//					for (vector<int>::iterator ite = Sprime.begin(); ite != Sprime.end(); ite++)
//						cout << *ite << " ";
//					cout << "Improved to " << bestobj <<
//						" at time " << ((double)(clock() - start_time)) / CLOCKS_PER_SEC << endl;
//					r_arr.push_back(s);
//					h_arr.push_back(j);
//					
//				}
//				while (!L.empty()) {
//					x[L.front().first][L.front().second].setLB(0);
//					x[L.front().first][L.front().second].setUB(1);
//					L.pop_front();
//				}
//			}
//		}
//
//		cout << "------------------------------------------------------------" << "\n";
//		cout << "r :" << r_arr[r_arr.size() - 1] << "\t" << "h: " << h_arr[h_arr.size() - 1] << endl;
//		vector<int> Sprime = get_sequence(cpx, x, N, S);
//		for (vector<int>::iterator ite = Sprime.begin(); ite != Sprime.end(); ite++)
//			cout << *ite << " ";
//		cout << "BestObj:------------------------" << bestobj << "\n";
//		cout << "init_FO:--------------------" << init_FO << "\n";
//		cout << "rbs_FO:----------------------" << rbs_FO << "\n";
//		cout << "------------------------------------------------------------" << "\n";
//		
//
//		if (rbs_FO == bestobj){
//			return 0;
//		}
//
//		if (rbs_FO != bestobj) {
//			float I = calculateI(init_FO, rbs_FO);
//			float Iprime = calculateI(init_FO, bestobj);
//			int r = r_arr[r_arr.size() - 1];
//			int h = h_arr[h_arr.size() - 1];
//
//			writeCSV(S_origin, S_prime, r, h, I, Iprime, "base.csv");
//		}
//		
//	}
//	
//}

void
read_jobs(const char *fname, vector<Job>& N)
{
	int dummy;
	N.resize(0);
	ifstream ifs(fname);
	if (ifs.is_open()) {
		Job buf;
		while (!ifs.eof()) {
			ifs >> buf.id;
			buf.id--;
			ifs >> buf.ptime[0] >> buf.ptime[1];
			/*cout<<"Here"<<endl;
			cout<<buf.ptime[0]<<"\t"<<buf.ptime[1]<<endl;*/
			if (!ifs.eof())
				N.push_back(buf);
		}
	}
	else {
		char msg[128];
		snprintf(msg, 127, "read_jobs(): cannot open %s", fname);
		throw(msg);
	}
}


float
read_sequence(const char *fname, vector<int>& S)
{
	ifstream ifs(fname);
	int obj;

	if (ifs.is_open()) {
		ifs >> obj;
		for (int i = 0; i < S.size(); ++i)
			ifs >> S[i];
	}
	else {
		char buf[128];
		snprintf(buf, 127, "read_sequence(): cannot open %s", fname);
		throw(buf);
	}
	return float(obj);
}


int main(int argc, char *argv[])
{
	int res = EXIT_SUCCESS;
	try {
		if (argc < 4) {
			throw("Please provide file name and random seed");
		}

		srand(atoi(argv[2]));
		double tlim = atof(argv[3]);
		vector<Job> N;
		read_jobs(argv[1], N);

		const char *ext = (argc > 4) ? argv[4] : "rbs";

		cout << N.size() << " jobs" << endl;

		IloEnv env;
		IloModel model(env);

		IloIntVarArray x[MAX_JOBS];
		for (int i = 0; i < N.size(); ++i) {
			char buf[128];
			x[i] = IloIntVarArray(env, N.size(), 0.0, 1.0);
			for (int j = 0; j < N.size(); ++j) {
				snprintf(buf, 127, "x(%d,%d)", i, j);
				x[i][j].setName(buf);
			}
		}

		IloNumVarArray Ctime[2];
		Ctime[0] = IloNumVarArray(env, N.size(), 0.0, IloInfinity);
		Ctime[1] = IloNumVarArray(env, N.size(), 0.0, IloInfinity);
		for (int i = 0; i < N.size(); ++i) {
			char buf[128];
			snprintf(buf, 127, "C(0,%d)", i);
			Ctime[0][i].setName(buf);
			snprintf(buf, 127, "C(1,%d)", i);
			Ctime[1][i].setName(buf);
		}

		model.add(IloMinimize(env, IloSum(Ctime[1])));

		for (int i = 0; i < N.size(); ++i) {
			IloExpr e(env);
			for (int j = 0; j < N.size(); ++j) {
				e += x[i][j];
			}
			model.add(e == 1.0);
			e.end();
		}

		for (int j = 0; j < N.size(); ++j) {
			IloExpr e(env);
			for (int i = 0; i < N.size(); ++i) {
				e += x[i][j];
			}
			model.add(e == 1.0);
		}


		for (int pos = 0; pos < N.size(); ++pos) {
			IloExpr tmp(env), tmp2(env), tmp3(env);
			tmp.clear();
			tmp2.clear();
			tmp3.clear();
			for (int i = 0; i < N.size(); ++i) {
				tmp += N[i].ptime[0] * x[i][pos];
				tmp2 += N[i].ptime[1] * x[i][pos];
				tmp3 += N[i].ptime[1] * x[i][pos];
			}
			if (!pos) {
				model.add(Ctime[0][0] >= tmp);
				model.add(Ctime[1][0] >= Ctime[0][0] + tmp2);
			}
			else {
				model.add(Ctime[0][pos] >= Ctime[0][pos - 1] + tmp);
				model.add(Ctime[1][pos] >= Ctime[1][pos - 1] + tmp2);
				model.add(Ctime[1][pos] >= Ctime[0][pos] + tmp3);
			}
		}
		IloCplex cpx(model);

		cpx.exportModel("pippo.lp");
		//cpx.setParam(IloCplex::TiLim, 20.0);
		cpx.setParam(IloCplex::MIPDisplay, 0);
		cpx.setParam(IloCplex::Param::ParamDisplay, 0);
		cpx.setParam(IloCplex::EpGap, 0);
		/*
		cpx.solve();
		int cur_best_obj=(int) cpx.getObjValue();
		*/
		vector<int> S(N.size());

		char ubname[128];
		snprintf(ubname, 127, "%s.%s", argv[1], ext);
		cout << ubname << endl;
		float cur_best_obj = read_sequence(ubname, S);

		init_FO = cur_best_obj;	//S become S with rbs
		cout << "Init_FO:----------------------------" << init_FO;
		cout << cur_best_obj << endl;//cur_best_obj = S rbs FO
		initial_obj = cur_best_obj;

		clock_t t_start = clock();
		search(cpx, x, N, S, cur_best_obj, tlim);

		if (initial_obj < cur_best_obj) {
			cout << "Current FO is greater than initial FO" << endl;
			exit(0);
		}
		cout << "INITIALOBJ=" << initial_obj << endl;
		cout << "BESTOBJ=" << cur_best_obj << endl;
		cout << "Total time=" << ((double)(clock() - t_start) / CLOCKS_PER_SEC) << endl;
		cout << "Avg subproblem time=" << avg_sp_time / sp_cnt << endl;
		cout << "Max subproblem time=" << max_sp_time << endl;

		char sfname[128];
		snprintf(sfname, 127, "%s.seq", argv[1]);
		ofstream ofs(sfname);
		if (ofs.is_open()) {
			ofs << cur_best_obj << "  ";
			for (int i = 0; i < N.size(); i++) {
				ofs << S[i] << " ";
			}
			ofs << "\n";
			/*ofs << r_arr[r_arr.size() - 1] << " ";
			ofs << h_arr[h_arr.size() - 1] << " ";
			ofs << endl;
		}
		for (auto i = r_arr.begin(); i != r_arr.end(); ++i)
			std::cout << *i << ' ';
		cout << "\n" << endl;
		for (auto i = h_arr.begin(); i != h_arr.end(); ++i)
			std::cout << *i << ' ';*/
		}
	}

	catch (const char *s) {
		cerr << s << endl;
		res = EXIT_FAILURE;
	}
	catch (IloException e) {
		cerr << e << endl;
		res = EXIT_FAILURE;
	}/*
	catch(...) {
	  cerr<<"Unhandled exception, my friend!"<<endl;
	  res=EXIT_FAILURE;
	}
	 */
	return res;
}
