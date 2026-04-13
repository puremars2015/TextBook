# 進出口API規格書

## 查詢進櫃單
- 端點:/api/TabContainerExport/EX_Goods_Container_Query
- 方法:GET
- sample request:
    ```
        https://oci-mes01.webpromaterials.com/mes-api-v2/api/TabContainerExport/EX_Goods_Container_Query?ContainerNo=00250013C1&GoodsNo=0&ContainerLocation=0&ContainerDate=0&ContainerSize=0&ContainerCod=0&InDate=0&OutDate=0&ID=0&Modify_Emp=0&ActionFlag=M2
    ```
- parameters:
    ```
    ContainerNo=00250013C1&GoodsNo=0&ContainerLocation=0&ContainerDate=0&ContainerSize=0&ContainerCod=0&InDate=0&OutDate=0&ID=0&Modify_Emp=0&ActionFlag=M2
    ```
- response:
    ```
    {"statusCode":200,"exgoodscontainerquery":[{"containerNo":"00250013C1","goodsNo":"00250013","trucker":"欣德路通運股份有限公司","containerLocation":"WPY","customer":"AEON","so":"0040","vslName":"EVER PRIMA 0351-442N","carrier":"EMC","destinationPort":"KOBE, JAPAN","closeDate":"2026-01-02","containerPlaceIn":"KAO-29 高雄S3","containerPlaceOut":"KAO-29 高雄S3","modify_Emp":"0","modify_Date":"01/10/2026 21:06:16"}]}
    ```