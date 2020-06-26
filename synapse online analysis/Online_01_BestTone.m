%01_BestTone

block = '/Users/majamilinkovic/Documents/MATLAB/tdt/Froggy_14/Block-1'


%for c= 1:12
    SortCode = []; % unit id(s) or empty for all units

    Channel = 2;
    win=[0.0 .1];
    binsize = 0.001;

    mwin = [0.01 0.05]; % measurement window
    % mwin = win;

    % For localization field estimation
    PARAM1 = 'freq';
    PARAM2 = 'atte';



    %%
 %   data = TDT2mat(tdt.tank,tdt.block,'type',[2 3],'silent',true); %load data from tdt tank block

    data = TDTbin2mat(block)
 
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

    trials = trials / binsize; %to get spk/s

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
    
    figure;
    for k1=1:12
        subplot(3, 4, k1)
        mPSTH = squeeze(mean(PSTH(:,:,ind),2)); %get rid of dimension, after averaging bins within measurement window into one
        shadedErrorBar(uX.',mPSTH.',{@mean,@(x) std(x)/sqrt(size(x, 1))},'lineprops',{'k-o','markerfacecolor','k'});
        %shadedErrorBar(uX.',mean(mPSTH,2),nanstd(mPSTH')/sqrt(41),'lineprops',{'k-o','markerfacecolor','k'});

        set(gca,'ydir','normal', 'ylim', [0, inf]);
        set(gca, 'xscale', 'log', 'xtick', uX(1:8:end), 'xticklabel', uX(1:8:end)/1e3, 'xlim', [uX(1),uX(end)]);
        junk=nanmean(mPSTH,2);
        [m id]=max(junk);
        frqMax= uX(id);
       % title(gca,sprintf('Mean spikes/s of Frequency responses across repetitions, Window = [%0.3f %0.3f] \n best fr=%3.3f',mwin,frqMax));
        ch_label = sprintf('Channel %d', k1);
        xL = xlim;
        yL = ylim;
        text(0.45,0.9, ch_label, 'Units','Normalized');
    end
    sgtitle('Mean spikes/s of Frequency responses across repetitions');
    
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
    xlabel('Frequency (kHZ)')
    ylabel('Average Spikes/s')

    
    
    figure;

    for k2=1:12
        subplot(3, 4, k2)
        [peakL,peakTime]=max(PSTH,[],3); %extract peak latency, and the bin number of the peak latency within the measurement window
        peakTimeT = (((peakTime*binsize)+mwin(1))*1000); %convert peakTime to milliseconds after stim onset and transposing for shadedErrorBar function
        plot(uX,peakTimeT);
        grid on;
        set(gca,'ydir','normal', 'ylim', [0, inf]);
        set(gca, 'xscale', 'log', 'xtick', uX(1:8:end), 'xticklabel', uX(1:8:end)/1e3, 'xlim', [uX(1),uX(end)]);
        ch_label = sprintf('Channel %d', k2);
        xL = xlim;
        yL = ylim;
        text(0.45,0.9, ch_label, 'Units','Normalized');

     %   xlabel('Frequency (kHZ)');
     %   ylabel('Latency (ms)'); %across dbSPL repetitions
    end
    %title(gca,sprintf('Peak Latency of Frequency responses across repetitions, Window = [%0.3f %0.3f]',mwin));
    sgtitle('Peak Latency of Frequency responses across repetitions');

    %get positions to center the axis labels
    h1=subplot(3,4,1); % top row, left corner
    h2=subplot(3,4,4); % top row, right corner
    h3 = subplot(3,4,9);% bottom row, left corner
    h4 = subplot(3,4,12); % bottom row, right corner
    
    p1=get(h1,'position');
    p2=get(h2,'position');
    p3=get(h3,'position');
    p4=get(h4,'position');
    
    height=p1(2)+p1(4)-p4(2);
    width=p4(1)+p4(3)-p3(1);
    h5=axes('position',[p3(1) p3(2) width height],'visible','off'); 
    h5.XLabel.Visible='on'
    h5.YLabel.Visible='on'
    
    axes(h5)
    xlabel('Frequency (kHZ)')
    ylabel('Latency (ms)')
    

%end