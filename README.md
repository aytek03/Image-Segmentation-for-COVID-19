# Image-Segmentation-for-COVID-19

Since december 2019, the entire world is facing a situation
of huge pandemic crisis due to a newly emerged
coronavirus-type disease (COVID-19). Although no vaccine
of COVID-19 is available yet, RT-PCR tests take an
important place in the diagnosis of COVID-19. Since it
suffers from high false negative rates and time consuming,
computed tomography (CT) is the one of the influential
technique to diagnose COVID-19. But it is hard for the
doctors (especially radiologists) to maintain an acceptable
level of attention when examining the CT images. Having
a computer-aided software from CT images will both save
time and help doctors to diagnose. In this paper, we analyze
the COVID-19 CT segmentation dataset, determine the
infection regions of dataset from the lungs and try to adjust
Inf-Net to more generalized method. We use Inf-Net
for the semantic segmentation model and we try to improve
its baseline. The structure of Inf-Net is created according
to Res2Net, and we expand its capabilities. We add these
networks which are iResNet50, ResNest50, ResNet50 and
ResNext50 to Inf-Net. These ResNet derivatives are easily
integrated and when the next network is VGG16, we change
Inf-Net’s baseline. Finally, we show the quantitative and
qualitative results and discussion about future work.
