close all
 
figure
pcolor(xt,yt,squeeze(SA(:,:,1))'); shading flat
set(gca,'YDir','normal')
caxis([34.5 35])
axis tight
 
figure
contour(xt,yt,squeeze(SA(:,:,1))', 500, 'k'); shading flat
set(gca,'YDir','normal')
axis tight
 
figure
pcolor(yt,zt,squeeze(SA(216,:,:))'); shading flat
caxis([34.5 35])
axis tight
set(gca,'YDir','reverse')




Ayz2d       = squeeze(Ayz(216,:,:))';
SA2d        = squeeze(SA(216,:,:))';
[yt2d,zt2d] = meshgrid(yt,zt);
index       = and(and(SA2d>=34.4, SA2d<34.5),yt2d<0);
index       = and(SA>=34.4, SA<34.5);
xx          = sum(index,3);
 
figure
imagesc(xx')
set(gca,'YDir','normal')
 
SA2d(pindex)
sum(Ayz2d(index))
 
figure
imagesc(yt,zt,index)
axis tight
 
close all
 
figure
pcolor(xt,yt,squeeze(SA(:,:,1))'); shading flat
set(gca,'YDir','normal')
caxis([34.5 35])
axis tight
 
figure
pcolor(xt,yt,squeeze(SA(:,:,1))'); shading flat
set(gca,'YDir','normal')
caxis([30 37])
axis tight
colormap('bone')
colorbar