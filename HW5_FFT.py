{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "HW5_FFT.py",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOW+hfid580c7DvA724SrbG",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Patiphan43/2020/blob/master/HW5_FFT.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "oEUz56yG1NyV",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import matplotlib.pyplot as plt\n",
        "import numpy as np\n",
        "\n",
        "def gaussian_kernel(size, sigma=1):\n",
        "    \"\"\"\n",
        "    Generate 2D Gaussian kernel\n",
        "    Input:  size = size of the Gaussian kernel\n",
        "            sigma = sigma of the Gaussian function\n",
        "    Output: 2D array of the Gaussian kernel\n",
        "    \"\"\"\n",
        "    n = size//2\n",
        "    xx, yy = np.meshgrid(range(-n,n+1), range(-n,n+1))\n",
        "    kernel = np.exp(- (xx**2 + yy**2) / (2*sigma**2))\n",
        "    kernel = kernel / kernel.sum()\n",
        "    return kernel\n",
        "\n",
        "\n",
        "def gaussian_blur_fft(image, kernel_size=5, sigma=1):\n",
        "    \"\"\"\n",
        "    Perform Gaussian blur on the image using FFT\n",
        "    Input:  image = the original image to perform Gaussian blur on\n",
        "            kernel_size = size of the Gaussian kernel\n",
        "            sigma = sigma of the Gaussian function\n",
        "    Output: Image after applied the Gaussian blur using FFT\n",
        "            Gaussian kernel in the frequency domain\n",
        "            Image in the frequency domain\n",
        "            Convolved image in the frequency domain\n",
        "    \"\"\"\n",
        "    kernel = gaussian_kernel(kernel_size, sigma)\n",
        " \n",
        "    pad_height = kernel.shape[0]//2\n",
        "    pad_width = kernel.shape[1]//2\n",
        "\n",
        "    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), 'edge')\n",
        "\n",
        "    kernel_fft = np.fft.fft2(kernel, s=padded_image.shape[:2], axes=(0, 1))\n",
        "\n",
        "    image_fft = np.fft.fft2(padded_image, axes=(0, 1))\n",
        "\n",
        "    convolved_fft = kernel_fft[:, :, np.newaxis] * image_fft\n",
        "\n",
        "    #find inverse of fft\n",
        "    inverse_fft = np.fft.ifft2(convolved_fft)\n",
        "\n",
        "    return inverse_fft, kernel_fft, image_fft, convolved_fft\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    img = plt.imread('cat.jpg')\n",
        "    img = img/255.\n",
        "    img_blur, kernel_fft, image_fft, convolved_fft = gaussian_blur_fft(img)\n",
        "\n",
        "    image_fft_shift = np.log( abs(np.fft.fftshift(image_fft).real) + 1 )\n",
        "    kernel_fft_shift = np.fft.fftshift(kernel_fft)\n",
        "    convolved_fft_shift = np.log( abs(np.fft.fftshift(convolved_fft).real) + 1 )\n",
        "\n",
        "    plt.figure()\n",
        "    plt.subplot(2,3,1)\n",
        "    plt.imshow(img)\n",
        "    plt.title('original')\n",
        "    plt.subplot(2,3,2)\n",
        "    plt.imshow(img_blur)\n",
        "    plt.title('blurred image')\n",
        "    \n",
        "    plt.subplot(2,3,4)\n",
        "    plt.imshow(kernel_fft.real)\n",
        "    plt.title('kernel')\n",
        "    plt.subplot(2,3,5)\n",
        "    plt.imshow(kernel_fft_shift.real)\n",
        "    plt.title('shifted kernel')\n",
        "    plt.subplot(2,3,6)\n",
        "    plt.imshow(image_fft_shift / image_fft_shift.max())\n",
        "    plt.title('shifted image fft magnitude')\n",
        "    plt.subplot(2,3,3)\n",
        "    plt.imshow(convolved_fft_shift / convolved_fft_shift.max())\n",
        "    plt.title('convolved image fft magnitude')\n",
        "    plt.show()"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}