% skipping synch tests
Screen('Preference', 'SkipSyncTests', 1);
% setting random seed
rng('Shuffle');
% opening the screen
[window, rect] = Screen('OpenWindow', 0);
% allowing transparency in the photos
Screen('BlendFunction', window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); %transparency
% hide cursor ;
HideCursor();

%% Define size of screen

 % width of the window
window_w = rect(3);
 % height of the window
window_h = rect(4);

currFolder = pwd;

framewidth = 5;
[imgs,map] = imread('in.gif', 'frames', 'all');
[h_frame, w_frame, cols, num_frames] = size(imgs);
numslices = ceil(w_frame/num_frames/framewidth);
nw = numslices*num_frames*framewidth;
newim = zeros(h_frame, nw);
for i = (1:num_frames)-1
    for j = (1:numslices)-1
        newim(:,(i+j*num_frames)*framewidth+1:(i+1+j*num_frames)*framewidth,:) = imgs(:,j*framewidth*num_frames+1:(j*num_frames+1)*framewidth,:,i+1);
    end
end
newim = ind2rgb(uint8(newim),map).*255;
imt = Screen('MakeTexture', window, newim);
overlay = zeros(h_frame, nw, 4);
for i = 0:numslices
    overlay(:,(i*num_frames+1)*framewidth+1:(i+1)*framewidth*num_frames,4) = ones(h_frame, framewidth*(num_frames-1));
end
ovt = Screen('MakeTexture', window, overlay*255);
Screen('DrawTexture', window, imt, [0 0 nw h_frame], [0 0 nw h_frame]);
Screen('Flip', window);
WaitSecs(1);
framerate = 60;
for j = 1:5
    for i = 0:num_frames*framewidth-1
        Screen('DrawTexture', window, imt, [0 0 nw h_frame], [0 0 nw h_frame]);
        Screen('DrawTexture', window, ovt, [0 0 nw h_frame], [i 0 nw+i h_frame]);
        Screen('DrawTexture', window, ovt, [0 0 nw h_frame], [i-nw-1 0 i-1 h_frame]);
        Screen('Flip', window);
        WaitSecs(1/framerate);
    end
end

Screen('CloseWindow');

