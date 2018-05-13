#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <unordered_set>
#include <deque>
#include <queue>
#include <stack>
#include <string.h>
#include <math.h>

using namespace std;

typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;

#define mp make_pair
#define pb push_back
#define all(x) x.begin(),x.end()
#define rall(x) x.rbegin(),x.rend()

const int MAX = 515;
ld dp[MAX][MAX];
int p[MAX][MAX];
int toId[MAX];
map<int,int> fromId;
int cnt = 1;

int newPoint(int l)
{
	if(!fromId[l])
	{
		toId[cnt]=l;
		fromId[l]=cnt++;
	}
	return fromId[l];
}

void retTrack(int x, int y, vector<int>& track)
{
	if(x==y)
	{
		track.pb(x);		
	}
	else
	{
		retTrack(x,p[x][y],track);
		if(x==p[x][y])
		{
			track.pb(y);
		}
		else
		{
			track.pop_back();
			retTrack(p[x][y],y,track);
		}
	}
}

void solve()
{
	ll a;
	for(int i=0;i<MAX;++i)
	{
		for(int j=0;j<MAX;++j)
		{
			dp[i][j]=1e9;
			p[i][j]=-1;
		}
	}

	cin>>a;

	int l,r,dist;

	for(int i=0;i<a;++i)
	{
		cin>>l>>r>>dist;

		l = newPoint(l);
		r = newPoint(r);
		dist = sqrt((ld)(dist));
		dp[l][r]=dist;
		dp[r][l]=dist;
		p[l][r]=l;
		p[r][l]=r;
	}

	for(int k=1;k<=a;++k)
	{
		for(int i=1;i<=a;++i)
		{
			for(int j=1;j<=a;++j)
			{
				int nwDist = dp[i][k]+dp[k][j];
				if(dp[i][j] > nwDist)
				{
					dp[i][j]=nwDist;
					p[i][j]=k;
				}
			}
		}
	}

	for(int i=1;i<cnt;++i)
	{
		for(int j=1;j<cnt;++j)
		{
			vector<int> curTrack;

			if(dp[i][j]!=1e9)
			{
				retTrack(i,j,curTrack);
			}
			cout<<toId[i]<<" "<<toId[j]<<" ";
			cout<<curTrack.size()<<" ";
			for(auto it = curTrack.begin();it!=curTrack.end();++it)
			{
				cout<<toId[*it]<<" ";
			}
			cout<<endl;
		}
	}
}	

#define name "strings"

int main() {
	ios_base::sync_with_stdio(false);
	//freopen(name".in","r",stdin); freopen(name".out","w",stdout);
	freopen("segment.txt","r",stdin); freopen("tracks.txt","w",stdout);
	cout.setf(ios::fixed);
	cout.precision(4);
	solve();

	return 0;
}