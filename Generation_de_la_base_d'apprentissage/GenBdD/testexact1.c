#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include <process.h>

#define depart 100
#define taille_max 100
#define pas 200
#define time_limite 120

unsigned long int iterations=2000;

float tpsbsr,tempsP;
unsigned long int ubbsr,opt,lb,sumri,optchu,lbchu,imp;
float range,alpha;
int jouechu=0,joue=0,jouebest=1,jouedepth=0,jouewidth=0;
long int CutAb_min,CutAb_max,CutAb, CutDb,CutDb_min,CutDb_max;
long int CutAd_min,CutAd_max,CutAd, CutDd,CutDd_min,CutDd_max;
long int CutAw_min,CutAw_max,CutAw, CutDw,CutDw_min,CutDw_max;
double CutAw_moy,CutDw_moy;
double CutAd_moy,CutDd_moy;
double CutAb_moy,CutDb_moy;

long int generer(long int nbtrav);


long int generer(long int nbtrav)
{
 long int i;
 long int ri,pi[taille_max],som=0;
 FILE *fichier;
 
 fichier=fopen("data.txt","wt");
 sumri=0;
 for (i=0;i<nbtrav;i++)
 {
  pi[i]=((float)rand()/(float)RAND_MAX)*99+1;
  ri=((float)rand()/(float)RAND_MAX)*99+1;
  fprintf(fichier,"%ld %ld %ld\n",i+1,ri,pi[i]);
 }
 fclose(fichier);
 return(sumri);
}

void main(void)
{
 long int i,j,lbchu,optchu,k;
 float tpschu;
 int t;
 FILE *fichier;

 double permin,permoy,permax,ndc_moy,ndp_moy,ndb_moy,ndd_moy,ndw_moy,tpc_moy,tpp_moy,tpc_min,tpc_max,tpp_min,tpp_max,tpd_min,tpd_moy,tpd_max,tpb_min,tpb_moy,tpb_max,tpw_min,tpw_moy,tpw_max;
 long int ndc_min, ndc_max, ndp_min,ndp_max,ndc,ndp;
 long int ndb_min, ndb_max, ndd_min,ndd_max,ndw_min,ndw_max;
 long int ag_ndc_min,ag_ndp_min,ag_ndb_min,ag_ndd_min,ag_ndw_min;
 long int ag_ndc_max,ag_ndp_max,ag_ndb_max,ag_ndd_max,ag_ndw_max;
 double ag_ndc_moy,ag_ndp_moy,ag_ndb_moy,ag_ndd_moy,ag_ndw_moy;
 double ag_tc_moy,ag_tp_moy,ag_tb_moy,ag_td_moy,ag_tw_moy;
 double ag_tc_min,ag_tp_min,ag_tb_min,ag_td_min,ag_tw_min;
 double ag_tc_max,ag_tp_max,ag_tb_max,ag_td_max,ag_tw_max;

 fichier = fopen("Database.txt", "wt");
 fprintf(fichier, "File structure\n");
 fprintf(fichier, "n r h PerImp PerImpSolInit (pi1,pi2)S (pi1,pi2)BestS\n");
 fclose(fichier);


 for (i=depart;i<=taille_max;i+=pas)
 {
  srand(time(NULL));
  
  printf("Nombre de travaux : %ld\n",i);
  for (j=0;j<iterations;j++)
  {
   printf("It�ration n�%ld\n",j+1);
   generer(i);

   printf("Running the matheuristic...\n");
   spawnl(P_WAIT,"MatheuristicGB.exe","MatheuristicGB.exe","data.txt","1","1800",NULL);
   fichier = fopen("Database.txt", "at+");
   fprintf(fichier, "\n");
   fclose(fichier);
  }
 }
 }
