%% Online_FRF

%tdt = TDT_TTankInterface; 
%tdt.tank = 'E:\TANKS\BLAKE\SUE_ELLEN\MALIBU_MAP';
%tdt.block = 'Block-1';

block = '/Users/majamilinkovic/Documents/MATLAB/tdt/Froggy_14/Block-2';
%%

Channel = 4;
SortCode = []; % unit id(s) or empty for all units


win=[0.0 .1]; %window of 100ms
binsize = 0.001; %binsize of 1ms

mwin = [0.01 0.05]; % measurement window
% mwin = win;

% For localization field estimation
PARAM1 = 'freq';
PARAM2 = 'atte';



%%
%swap to TDTbin2mat
%data = TDT2mat(tdt.tank,tdt.block,'type',[2 3],'silent',true); %load data

data = TDTbin2mat(block); % takes as input the block path

Fs = data.snips.eNeu.fs; %sampling rate


uChan = unique(data.snips.eNeu.chan); %channel selected
uSort = unique(data.snips.eNeu.sortcode); %online spike sorted data

X = data.epocs.(PARAM1).data; uX = unique(X); %data from parameter 1, frequencies presented
Y = data.epocs.(PARAM2).data; uY = unique(Y); %data from parameter 2, amplitudes presented

ons = data.epocs.(PARAM1).onset; %onset times of paramater 1 (frequencies)

ts = data.snips.eNeu.ts; %timestamps


if isempty(SortCode)
    ind_sc = true(size(data.snips.eNeu.sortcode)); %boolean of snippets counted, where 1=true
else
    ind_sc = ismember(data.snips.eNeu.sortcode,SortCode); %add all snippets that exist, 
end
ind_ch = data.snips.eNeu.chan == Channel; %labelled channel number

ts = ts(ind_sc & ind_ch); %add snippets from the labelled channel to the timestamps

if isempty(ts)
    fprintf(2,'NO DATA on channel %d, sort %d\n',Channel,SortCode); %if timestamps dont exist, print that
    return
end

clear data

binvec = win(1):binsize:win(2)-binsize; %create a vector of binsizes within the specified timeframe


nX = length(uX); %number of frequencies presented
nY = length(uY); %number of amplitudes presented
trials = zeros(length(ons),length(binvec)); %matrix of trials, onset times on the x axis and binvector on the y axis
for i = 1:length(ons) %for each snippet onset time
    ind = (ts >= ons(i) + win(1)) & (ts < ons(i) + win(2) - binsize); %ind=index of snippets between the ith window
    trials(i,:) = histc(ts(ind)-ons(i),binvec); %histogram of snippet latencies, calculated by snippet onset minus stimulus onset
end
 plot(nanmean(trials))
% hold on;
trials = trials / binsize; %divide by binsize to get spk/s on the y-axis
plot(nanmean(trials))

PSTH = zeros(length(uX),length(uY),length(binvec)); %3d array, frequency and amplitude for each bin
for x = 1:nX
    for y = 1:nY %for each frequency and amplitude combination
        ind = uX(x) == X & uY(y) == Y; %index each frequency and amplitude
        PSTH(x,y,:) = mean(trials(ind,:)); %create an average across repetitions of snippet responses to frequency and amplitude, NOT IN ORDER
    end
end

% Plot stuff
f = findobj('type','figure','-and','name','FRF');
if isempty(f), f = figure('name','FRF','color','w'); end
figure(f); delete(get(f,'children'));


ind = binvec >= mwin(1) & binvec <= mwin(2); %index bins inside measurement window

mPSTH = flipud(squeeze(mean(PSTH(:,:,ind),3))'); %get rid of third dimension (time), after averaging bins within measurement window = 1. average spk/s across bins for each Hz/dbSPL combo
%Commented out: boxed version
%{
subplot(211)
pcolor(uX,uY,mPSTH);%plots "chaotic" PSTH data into order
set(gca,'ydir','normal');
set(gca,'clim',[0 max(mPSTH(:))]);
set(gca, 'xscale', 'log', 'xtick', uX(1:6:end), 'xticklabel', uX(1:6:end)/1e3 )
title(gca,sprintf('Window = [%0.3f %0.3f]',mwin));
xlabel('Frequency (kHZ)');
ylabel('dBSPL');
colorbar
%}
%%%%%%%add colorbar legend

figure;
for k1=1:12
    subplot(3, 4, k1)
    mv = max(mPSTH(:)); %grabbing maximum value from mPSTH
    cPSTH = interp2(mPSTH,3); %2d interpolation, halving intervals 3 times in each dimension. visually, produces further smoothing
    imagesc(uX,uY,(cPSTH/max(cPSTH(:)))*mv); %normalization, max spike from smoothed data is same as raw data
    set(gca,'ydir','normal');
    set(gca,'clim',[0 mv]);
    set(gca, 'xscale', 'log', 'xtick', uX(1:6:end), 'xticklabel', uX(1:6:end)/1e3, 'xlim', [uX(1),uX(end)]);
    ch_label = sprintf('Channel %d', k1);
    xL = xlim;
    yL = ylim;
    text(0.45,0.9, ch_label, 'Units','Normalized');
    colorbar
end

sgtitle(sprintf('Window = [%0.3f %0.3f]',mwin));

%get positions to center the axis labels
    a1=subplot(3,4,1); % top row, left corner
    a2=subplot(3,4,4); % top row, right corner
    a3 = subplot(3,4,9);% bottom row, left corner
    a4 = subplot(3,4,12); % bottom row, right corner
    
    pos1=get(a1,'position');
    pos2=get(a2,'position');
    pos3=get(a3,'position');
    pos4=get(a4,'position');
    
    height=pos1(2)+pos1(4)-pos4(2);
    width=pos4(1)+pos4(3)-pos3(1);
    a5=axes('position',[pos3(1) pos3(2) width height],'visible','off'); 
    a5.XLabel.Visible='on'
    a5.YLabel.Visible='on'
    
    axes(a5)

xlabel('Frequency (kHZ)');
ylabel('dBSPL');

