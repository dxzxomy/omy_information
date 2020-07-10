    app.run(function($rootScope,$uibModal) {
    $rootScope.$on('$locationChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
        //获取 href 属性中在井号“#”后面的分段
        var path = window.location.hash;
        path = path.substring(path.lastIndexOf("\/")+1,path.length);
        if(path.match(RegExp('^[0-9]*$'))){
            $rootScope.isWho = path;
            path = window.location.href;
            path = path.substring(path.lastIndexOf("\/", path.lastIndexOf("\/") - 1) + 1,path.length-2);
        }
        $rootScope.channelPath = path;

        //统计分析
        var statistics = ["attentionStatistics","bindingStatistics","elecBusinessStatistics","elecBusinessDetail","powerRepairStatistics","customerAppealStatistics"];

        //需求管理
        var demand = ["newDemand","pendDemand","demandList","examineDemand"];
        if(checkNotNull(path)){
            if(path.match(RegExp("versionHome"))){
                //首页
                $rootScope.channelIndex = "versionHome";
            }else if(statistics.indexOf(path)>-1){
                //统计分析
                commonSet('#accordion');
            }else if(demand.indexOf(path)>-1){
                //需求管理
                commonSet('#accordion7');
            }
        }
        //共用的判断条件
        function commonSet(firstMenu) {
            $rootScope.channelIndex = firstMenu;
        }

    })
})