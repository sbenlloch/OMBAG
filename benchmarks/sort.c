#include <stdio.h>
#include <stdlib.h>

void permuta(int *x, int *y){
    int temp = *x;
    *x = *y;
    *y = temp;
}

int sonIguales(int array1[], int array2[], int size){
    int i;
    for(i = 0; i < size - 1; i++){
        if(array1[i] != array2[i]){
            return 0;
        }
    }

    return 1;
}

void bubbleSort(int array[], int size){
    int i, j;
    for (i = 0; i < size-1; i++)     

        for (j = 0; j < size-i-1; j++)
            if (array[j] > array[j+1])
                permuta(&array[j], &array[j+1]);
}

void merge(int array[], int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];
    for (i = 0; i < n1; i++)
        L[i] = array[l + i];
    for (j = 0; j < n2; j++)
        R[j] = array[m + 1 + j];

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            array[k] = L[i];
            i++;
        }
        else {
            array[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        array[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        array[k] = R[j];
        j++;
        k++;
    }
}


void mergeSort(int array[], int l, int r){
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(array, l, m);
        mergeSort(array, m + 1, r);
        merge(array, l, m, r);
    }
}

int middle (int array[], int l, int h){
    int pivot = array[h];
    int i = (l - 1);
    for (int j = l; j <= h - 1; j++)
    {
        if (array[j] < pivot)
        {
            i++;
            permuta(&array[i], &array[j]);
        }
    }
    permuta(&array[i + 1], &array[h]);
    return (i + 1);
}

void quickSort(int array[], int l, int h){
    if (l < h)
    {

        int pivote = middle(array, l, h);
        quickSort(array, l, pivote - 1);
        quickSort(array, pivote + 1, h);
    }
}

void imprimir(int array[], int size)
{
    int i;
    for (i = 0; i < size; i++){
        printf("%d ", array[i]);
    }
    printf("\n");
}

void mezclar( int array[], int size ){
    for (int i = size-1; i > 0; i--){
        int j = rand() % (i+1);
        permuta(&array[i], &array[j]);
    }
}

int main(){
    
    int size = 1000;
    int vector[size]; //generado aleatoriamente con talla size
    int i;
    for (i = 0; i < size; i++) {
        vector[i] = rand();
    }

    
    int *vector1 = vector;
    mezclar(vector1, size);
    //imprimir(vector1, size);
    int *vector2 = vector;
    mezclar(vector2, size);
    //imprimir(vector2, size);
    int *vector3 = vector;
    mezclar(vector3, size);
    //imprimir(vector3, size);
    bubbleSort(vector1, size);
    mergeSort(vector2, 0, size - 1);
    quickSort(vector3, 0, size - 1);

    if (sonIguales(vector1 , vector2, size)){
        printf("True\n");
        //imprimir(vector1, size);
        //imprimir(vector2, size);
        //imprimir(vector3, size);
        return 0;
        
    }
    if (sonIguales(vector3 , vector2, size)){
        printf("True\n");
        //imprimir(vector1, size);
        //imprimir(vector2, size);
        //imprimir(vector3, size);
        return 0;
        
    }
    if (sonIguales(vector1 , vector3, size)){
        printf("True\n");
        //imprimir(vector1, size);
        //imprimir(vector2, size);
        //imprimir(vector3, size);
        return 0;
        
    }
    printf("False\n");
    return 1;
}