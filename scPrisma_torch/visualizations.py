import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from algorithms import *
from sklearn.manifold import LocallyLinearEmbedding , TSNE , Isomap
import seaborn as sns
from sklearn.metrics.pairwise import  euclidean_distances
import scanpy as sc


def plot_diag(D):
    T = D.diagonal()
    x = range(len(T))
    plt.plot(x,T)
    plt.show()

    pass

def painted_lle_orig(V, title="LLE"):
    model = LocallyLinearEmbedding(n_neighbors=150, n_components=3, method='modified',
                                   eigen_solver='dense')
    out = model.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(out[:, 0], out[:, 1], out[:, 2], c=range(len(V[:,0])))  # , **colorize)        plt.show()
    plt.show()
    pass

def pca_3d(V):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=3)
    pca.fit(V)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(V), columns=['PCA%i' % i for i in range(3)])

    # Plot initialisation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'],  s=60, c= range(V.shape[0]))

    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    zAxisLine = ((0, 0), (0,0), (min(result['PCA2']), max(result['PCA2'])))
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')

    # label the axes
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    plt.show()
    pass

def pca_3d_painted(V , paint):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=3)
    pca.fit(V)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(V), columns=['PCA%i' % i for i in range(3)])

    # Plot initialisation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax1 =ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'],c=paint, s=60)
    plt.colorbar(ax1)
    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    zAxisLine = ((0, 0), (0,0), (min(result['PCA2']), max(result['PCA2'])))
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')

    # label the axes
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    plt.show()
    pass


def painted_tsne_2D(V, clusters):
    tsne = TSNE(n_components=2, random_state=123)
    z = tsne.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(z[:, 0], z[:, 1] ,  c=clusters)  # , **colorize)        plt.show()
    plt.show()
    pass

def painted_isomap_2D(V, clusters):
    iso = Isomap(n_components=2)
    z = iso.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(z[:, 0], z[:, 1] ,  c=clusters)  # , **colorize)        plt.show()
    plt.show()
    pass

def painted_lle_2D(V, num_groups,groups_start, group_end , group_label , title="LLE 2D"):
    iso = LocallyLinearEmbedding(n_components=2 , n_neighbors=40)
    z = iso.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot()
    for i in range(num_groups):
        ax.scatter(z[groups_start[i]:group_end[i], 0], z[groups_start[i]:group_end[i], 1] ,  label=group_label[i])  # , **colorize)        plt.show()
    plt.legend()
    plt.title(title)
    plt.show()
    pass

def painted_lle_3D(V, num_groups,groups_start, group_end , group_label , title="LLE 3D"):
    iso = LocallyLinearEmbedding(n_components=3 , n_neighbors=40)
    z = iso.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i in range(num_groups):
        ax.scatter(z[groups_start[i]:group_end[i], 0], z[groups_start[i]:group_end[i], 1] , z[groups_start[i]:group_end[i], 2] ,  label=group_label[i])  # , **colorize)        plt.show()
    plt.legend()
    plt.title(title)
    plt.show()
    pass

def lle_2D(V , title="LLE 2D"):
    iso = LocallyLinearEmbedding(n_components=2 , n_neighbors=40)
    z = iso.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(V[:, 0], V[:, 1] )  # , **colorize)        plt.show()
    plt.legend()
    plt.title(title)
    plt.show()
    pass


def pca_2d_d_colorbar(data,color,title):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=2)
    pca.fit(data)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(data), columns=['PCA%i' % i for i in range(2)])

    # Plot initialisation
    fig = plt.figure()
    cmap = plt.get_cmap('RdBu', np.max(color)-np.min(color)+1)
    ax = fig.add_subplot()
    sc = ax.scatter(result['PCA0'], result['PCA1'],  s=15 , c=color,cmap=cmap)
    cax = plt.colorbar(sc, ticks=np.arange(np.min(color),np.max(color)+1))
    plt.title(title)
    # make simple, bare axis lines through space:


    #get discrete colormap
    # set limits .5 outside true range
    #pca_plot = plt.matshow(data,cmap=cmap,vmin = np.min(data)-.5, vmax = np.max(data)+.5)
    #tell the colorbar to tick at integers
    #cax = ax.set_colorbar(sc, ticks=np.arange(np.min(color),np.max(color)+1))
    # label the axes
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    plt.show()
    pass

def ranged_pca_2d(V , color,title="PCA Plot" , dis_colorbar=False):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=2)
    pca.fit(V)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(V), columns=['PCA%i' % i for i in range(2)])

    # Plot initialisation
    fig = plt.figure()
    ax = fig.add_subplot()
    sc = ax.scatter(result['PCA0'], result['PCA1'],  s=15 , c=color)
    if not(dis_colorbar):
        cbar = plt.colorbar(sc)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(18)
    plt.title(title)
    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    plt.tick_params(labelsize=18)
    # label the axes
    ax.set_xlabel("PC1", fontsize=18)
    ax.set_ylabel("PC2" , fontsize=18)
    plt.show()
    pass

def scalled_ranged_pca_2d(V , color,title="PCA Plot" , vmin=0, vmax=1, dis_colorbar=False):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=2)
    pca.fit(V)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(V), columns=['PCA%i' % i for i in range(2)])

    # Plot initialisation
    fig = plt.figure()
    ax = fig.add_subplot()
    sc = ax.scatter(result['PCA0'], result['PCA1'],  s=15 , c=color , vmax=vmax, vmin=vmin)
    if not(dis_colorbar):
        cbar = plt.colorbar(sc)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(18)
    plt.title(title , fontsize=18)
    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    plt.tick_params(labelsize=18)
    # label the axes
    ax.set_xlabel("PC1", fontsize=18)
    ax.set_ylabel("PC2" , fontsize=18)
    plt.show()
    pass

def ranged_lle_2D(V, clusters):
    lle = LocallyLinearEmbedding(n_components=2 , n_neighbors=30)
    z = lle.fit_transform(V)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax1 = ax.scatter(z[:, 0], z[:, 1] ,  c=clusters , s=8)  # , **colorize)        plt.show()
    plt.colorbar(ax1)
    plt.show()
    pass

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        #return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        return '{p:.2f}%'.format(p=pct)
    return my_autopct

def visualize_distances(matrix,title="Distance matrix visualization"):
    C =euclidean_distances(matrix)
    n= matrix.shape[0]
    plt.matshow(C, cmap="Reds")
    ax = plt.gca()
    # Set the plot labels
    xlabels = ["%d" % i for i in range(n + 1)]
    ylabels = ["%d" % i for i in range(n + 1)]
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    # Add text to the plot showing the values at that point
    for i in range(n):
        for j in range(n):
            plt.text(j, i, int(100*C[i, j])/100, horizontalalignment='center', verticalalignment='center')
    plt.title(title)
    plt.show()

def plt_mean_std_gene_liver(adata, gene, up_lim=0.6, down_lim=-0.05, title="", color='b'):
    print(1111)
    ct_list = ['0', '6', '12', '18']
    mean_array = np.zeros(4)
    std_array = np.zeros(4)
    for i, ct in enumerate(ct_list):
        adata_nr = (adata[adata.obs['ZT'].isin([ct])])
        mean_array[i] = float(np.mean(adata_nr[:, gene].X))
        std_array[i] = float(np.std(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, mean_array, 'k')
    plt.errorbar(ct_list, mean_array, std_array, linestyle='None', marker='*' , color = color)
    #plt.plot(ct_list, e_array, 'bo', color=color)  # ct_list, dbp_array, 'k')
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on raw " + title + " as a function of time")
    plt.ylabel("Gene expression")
    plt.xlabel("Circadian time")
    plt.show()
    layer_list = ['0', '1', '2', '3', '4', '5', '6', '7']
    layer_list = range(8)
    mean_array = np.zeros(8)
    std_array = np.zeros(8)
    for i, layer in enumerate(layer_list):
        adata_nr = (adata[adata.obs['layer'].isin([layer])])
        mean_array[i] = float(np.mean(adata_nr[:, gene].X))
        std_array[i] = float(np.std(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(layer_list, mean_array, 'k')
    plt.errorbar(layer_list, mean_array, std_array, linestyle='None', marker='*' , color = color)
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on " + title + " as a function of layer")
    plt.ylabel("Gene expression")
    plt.xlabel("Layer")
    plt.show()
    sc.tl.pca(adata)
    sc.pl.pca_scatter(adata, color=gene, title=("PCA of " + title + " painted by " + str(gene)))

    pass

def plt_mean_std_gene_liver(adata, gene, up_lim=0.6, down_lim=-0.05, title="", color='b'):
    print(1111)
    ct_list = ['0', '6', '12', '18']
    mean_array = np.zeros(4)
    std_array = np.zeros(4)
    for i, ct in enumerate(ct_list):
        adata_nr = (adata[adata.obs['ZT'].isin([ct])])
        mean_array[i] = float(np.mean(adata_nr[:, gene].X))
        std_array[i] = float(np.std(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, mean_array, 'k')
    plt.errorbar(ct_list, mean_array, std_array, linestyle='None', marker='*' , color = color)
    #plt.plot(ct_list, e_array, 'bo', color=color)  # ct_list, dbp_array, 'k')
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on raw " + title + " as a function of time")
    plt.ylabel("Gene expression")
    plt.xlabel("Circadian time")
    plt.show()
    layer_list = ['0', '1', '2', '3', '4', '5', '6', '7']
    layer_list = range(8)
    mean_array = np.zeros(8)
    std_array = np.zeros(8)
    for i, layer in enumerate(layer_list):
        adata_nr = (adata[adata.obs['layer'].isin([layer])])
        mean_array[i] = float(np.mean(adata_nr[:, gene].X))
        std_array[i] = float(np.std(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(layer_list, mean_array, 'k')
    plt.errorbar(layer_list, mean_array, std_array, linestyle='None', marker='*' , color = color)
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on " + title + " as a function of layer")
    plt.ylabel("Gene expression")
    plt.xlabel("Layer")
    plt.show()
    sc.tl.pca(adata)
    sc.pl.pca_scatter(adata, color=gene, title=("PCA of " + title + " painted by " + str(gene)))

    pass


def heatmap_crit(gene_list,cluster,crit):
    adata_raw = sc.read("SCN/" + cluster + "_raw" + ".h5ad")
    adata_en = sc.read("SCN/" +cluster + "_en" + ".h5ad")
    adata_filtered = sc.read("SCN/" +cluster + "_filtered" + ".h5ad")
    sc.pl.heatmap(adata_raw, gene_list, groupby=crit)  # , swap_axes=True)
    sc.pl.heatmap(adata_en, gene_list, groupby=crit)  # , swap_axes=True)
    sc.pl.heatmap(adata_filtered, gene_list, groupby=crit)  # , swap_axes=True)
    pass

def plt_mean_gene_group(clusters, gene, up_lim=0.6, down_lim=-0.05):
    ct_list = ['02', '06', '10', '14', '18', '22']
    e_array = np.zeros(6)
    plt.figure()
    plt.subplot(211)
    plt.ylim([down_lim, up_lim])
    color_list = ['cyan', 'coral', 'violet', 'olive']
    for j, cluster in enumerate(clusters):
        adata_raw = sc.read("SCN/" + cluster + "_raw" + ".h5ad")
        for i, ct in enumerate(ct_list):
            adata_nr = (adata_raw[adata_raw.obs['CT'].isin([ct])])
            e_array[i] = float(np.mean(adata_nr[:, gene].X))
        plt.plot(ct_list, e_array, '-gD', color=color_list[j],
                 label=cluster, )  # , 'k')#, 'bo')#,color='b')# ct_list, dbp_array, 'k')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                   fancybox=True, shadow=True, ncol=5)
        plt.xlabel("Circadian time")
        plt.ylabel("Mean " + gene + " expression")
        plt.title("Raw data - mean " + gene + " expression as a function of circadian time", y=1.05)
    plt.show()

    plt.figure()
    plt.subplot(211)
    plt.ylim([down_lim, up_lim])
    for j, cluster in enumerate(clusters):
        adata_filtered = sc.read("SCN/" + cluster + "_filtered" + ".h5ad")
        for i, ct in enumerate(ct_list):
            adata_nr = (adata_filtered[adata_filtered.obs['CT'].isin([ct])])
            e_array[i] = float(np.mean(adata_nr[:, gene].X))
        plt.plot(ct_list, e_array, '-gD', color=color_list[j],
                 label=cluster, )  # , 'k')#, 'bo')#,color='b')# ct_list, dbp_array, 'k')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                   fancybox=True, shadow=True, ncol=5)
        plt.xlabel("Circadian time")
        plt.ylabel("Mean " + gene + " expression")
        plt.title("Filtered signal - mean " + gene + " expression as a function of circadian time", y=1.05)
    plt.show()

    plt.figure()
    plt.subplot(211)
    plt.ylim([down_lim, up_lim])
    for j, cluster in enumerate(clusters):
        adata_en = sc.read("SCN/" + cluster + "_en" + ".h5ad")
        for i, ct in enumerate(ct_list):
            adata_nr = (adata_en[adata_en.obs['CT'].isin([ct])])
            e_array[i] = float(np.mean(adata_nr[:, gene].X))
        plt.plot(ct_list, e_array, '-gD', color=color_list[j],
                 label=cluster, )  # , 'k')#, 'bo')#,color='b')# ct_list, dbp_array, 'k')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                   fancybox=True, shadow=True, ncol=5)
        plt.xlabel("Circadian time")
        plt.ylabel("Mean " + gene + " expression")
        plt.title("Enhanced signal - mean " + gene + " expression as a function of circadian time", y=1.05)
    plt.show()
    pass


def plt_mean_gene(cluster, gene, up_lim=0.6, down_lim=-0.05):
    adata_raw = sc.read("SCN/" + cluster + "_raw" + ".h5ad")
    adata_en = sc.read("SCN/" + cluster + "_en" + ".h5ad")
    adata_filtered = sc.read("SCN/" + cluster + "_filtered" + ".h5ad")
    ct_list = ['02', '06', '10', '14', '18', '22']
    e_array = np.zeros(6)
    for i, ct in enumerate(ct_list):
        adata_nr = (adata_raw[adata_raw.obs['CT'].isin([ct])])
        e_array[i] = float(np.mean(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, e_array, 'k')
    plt.plot(ct_list, e_array, 'bo', color='b')  # ct_list, dbp_array, 'k')
    plt.ylim([down_lim, up_lim])
    plt.title("Mean "+ gene + " expression on raw " + cluster + " data")
    plt.ylabel("Gene expression", fontsize=14)
    plt.xlabel("Circadian time" , fontsize=14)
    plt.show()
    for i, ct in enumerate(ct_list):
        adata_nr = (adata_en[adata_en.obs['CT'].isin([ct])])
        e_array[i] = float(np.mean(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, e_array, 'k')
    plt.plot(ct_list, e_array, 'bo', color='r')  # ct_list, dbp_array, 'k')
    plt.title("Mean "+ gene + " expression on enhanced " + cluster + " data")
    plt.ylabel("Gene expression", fontsize=14)
    plt.xlabel("Circadian time" , fontsize=14)
    plt.ylim([down_lim, up_lim])
    plt.show()
    for i, ct in enumerate(ct_list):
        adata_nr = (adata_filtered[adata_filtered.obs['CT'].isin([ct])])
        e_array[i] = float(np.mean(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, e_array, 'k')
    plt.plot(ct_list, e_array, 'bo', color='g')  # ct_list, dbp_array, 'k')
    plt.title("Mean "+ gene + " expression on filtered " + cluster + " data")
    plt.ylabel("Gene expression", fontsize=14)
    plt.xlabel("Circadian time", fontsize=14)
    plt.ylim([down_lim, up_lim])
    plt.show()
    pass

def plot_covariance_matrix(A,title):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax1 = ax.imshow(A.dot(A.T))
    cbar = plt.colorbar(ax1)
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(18)
    plt.tick_params(labelsize=18)
    #plt.title(title)
    plt.show()
    pass

def plot_gene_list(adata, gene_list, color1='black', color2='r', title=''):
    for i in gene_list:
        try:
            plt.plot(range(adata.X.shape[0]), adata[:, i].X, label=i, color=color1)
            plt.plot(range(adata.X.shape[0]), savgol_filter(adata[:, i].X[:, 0], 25, 3), label=("Smoothed " + i),
                     color=color2)
            #plt.legend(fontsize=16)  # [i,("Smoothed " +i)]
            plt.title(str(title), fontsize=18)
            plt.xlabel("cell location at expression matrix" , fontsize=18)
            plt.ylabel(i+ " expression",fontsize=18)
            plt.tick_params(labelsize=18)
            plt.show()
        except:
            print(1)


def plt_mean_gene_liver(adata, gene, up_lim=0.6, down_lim=-0.05, title="", color='b'):
    print(1111)
    ct_list = ['0', '6', '12', '18']
    e_array = np.zeros(4)
    for i, ct in enumerate(ct_list):
        adata_nr = (adata[adata.obs['ZT'].isin([ct])])
        e_array[i] = float(np.mean(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(ct_list, e_array, 'k')
    plt.plot(ct_list, e_array, 'bo', color=color)  # ct_list, dbp_array, 'k')
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on raw " + title + " as a function of time")
    plt.ylabel("Gene expression")
    plt.xlabel("Circadian time")
    plt.show()
    layer_list = ['0', '1', '2', '3', '4', '5', '6', '7']
    layer_list = range(8)
    e_array = np.zeros(8)
    for i, layer in enumerate(layer_list):
        adata_nr = (adata[adata.obs['layer'].isin([layer])])

        e_array[i] = float(np.mean(adata_nr[:, gene].X))
    plt.figure()
    plt.subplot(211)
    plt.plot(layer_list, e_array, 'k')
    plt.plot(layer_list, e_array, 'bo', color=color)  # ct_list, dbp_array, 'k')
    plt.ylim([down_lim, up_lim])
    plt.title("Mean " + gene + " expression on " + title + " as a function of layer")
    plt.ylabel("Gene expression")
    plt.xlabel("Layer")
    plt.tick_params(labelsize=14)
    plt.show()
    sc.tl.pca(adata)
    plt.tick_params(labelsize=14)
    sc.pl.pca_scatter(adata, color=gene, title=("PCA of " + title + " painted by " + str(gene)))

    pass

def plots_liver(adata,title):
    sc.pp.neighbors(adata)
    sc.tl.pca(adata)
    sc.pl.pca_scatter(adata, color='layer' , title=("PCA of " + title + " painted by layer"), legend_fontsize='x-large')
    sc.pl.pca_scatter(adata, color='ZT' , title=("PCA of " + title + " painted by ZT"), legend_fontsize='x-large')
    sc.tl.tsne(adata)
    sc.pl.tsne(adata, color='ZT' , title=("TSNE of " + title + " painted by ZT"), legend_fontsize='x-large')
    sc.pl.tsne(adata, color='layer' , title=("TSNE of " + title + " painted by layer"), legend_fontsize='x-large')

    pass

def pca_2d_d_colorbar(data,color,title):
    sns.set_style("white")
    # Run The PCA
    pca = PCA(n_components=2)
    pca.fit(data)
    # Store results of PCA in a data frame
    result=pd.DataFrame(pca.transform(data), columns=['PCA%i' % i for i in range(2)])

    # Plot initialisation
    fig = plt.figure()
    cmap = plt.get_cmap('Set1', np.max(color)-np.min(color)+1)
    ax = fig.add_subplot()
    sc = ax.scatter(result['PCA0'], result['PCA1'],  s=15 , c=color,cmap=cmap)
    cax = plt.colorbar(sc, ticks=np.arange(np.min(color),np.max(color)+1))
    plt.title(title)
    # make simple, bare axis lines through space:


    #get discrete colormap
    # set limits .5 outside true range
    #pca_plot = plt.matshow(data,cmap=cmap,vmin = np.min(data)-.5, vmax = np.max(data)+.5)
    #tell the colorbar to tick at integers
    #cax = ax.set_colorbar(sc, ticks=np.arange(np.min(color),np.max(color)+1))
    # label the axes
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    plt.show()
    pass

def get_mean_ct_gene_liver(adata, gene):
    ct_list = ['0', '6', '12', '18']
    mean_array_ct = np.zeros(4)
    std_array = np.zeros(4)
    for i, ct in enumerate(ct_list):
        adata_nr = (adata[adata.obs['ZT'].isin([ct])])
        mean_array_ct[i] = float(np.mean(adata_nr[:, gene].X))
    return mean_array_ct

def get_mean_layer_gene_liver(adata, gene):
    layer_list = ['0', '1', '2', '3', '4', '5', '6', '7']
    layer_list = range(8)
    mean_array_layer = np.zeros(8)
    std_array = np.zeros(8)
    for i, layer in enumerate(layer_list):
        adata_nr = (adata[adata.obs['layer'].isin([layer])])
        mean_array_layer[i] = float(np.mean(adata_nr[:, gene].X))

    return mean_array_layer


def plt_mean_heatmap_gene_liver(adata, adata_cyclic_filtered , adata_cyclic_en,adata_linear_filtered , adata_linear_en,gene ):
    data = np.array([get_mean_ct_gene_liver(adata,gene),
                    get_mean_ct_gene_liver(adata_cyclic_filtered,gene),
                    get_mean_ct_gene_liver(adata_cyclic_en,gene),
                    get_mean_ct_gene_liver(adata_linear_filtered,gene),
                    get_mean_ct_gene_liver(adata_linear_en,gene)])
    df = pd.DataFrame(data, index=
                ['Raw data','Cyclic filtered','Cyclic enhanced','Linear filtered','Linear enhanced'], columns=['CT0','CT6','CT12','CT18'])
    ax = sns.heatmap(df, cmap='rocket_r').set(title= gene + " expression as a function of sampling CT")
    plt.tick_params(labelsize=14)
    ax.set_xlabel('Circadian timepoint', fontsize=14)

    #sns.set(font_scale=1.5)
    #ax.set_xlabel('Circadian timepoint')
    plt.show()

    data = np.array([get_mean_layer_gene_liver(adata,gene),
                    get_mean_layer_gene_liver(adata_cyclic_filtered,gene),
                    get_mean_layer_gene_liver(adata_cyclic_en,gene),
                    get_mean_layer_gene_liver(adata_linear_filtered,gene),
                    get_mean_layer_gene_liver(adata_linear_en,gene)])
    df = pd.DataFrame(data, index=
                ['Raw data','Cyclic filtered','Cyclic enhanced','Linear filtered','Linear enhanced'], columns=range(8))
    ax = sns.heatmap(df , cmap='rocket_r').set(title= gene + " expression as a function of layer")
    ax.set_xlabel('Zonation layer', fontsize=14)
    plt.show()

    pass
