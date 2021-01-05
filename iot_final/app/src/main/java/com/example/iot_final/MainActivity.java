package com.example.iot_final;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import com.google.gson.Gson;
import com.mediatek.mcs.Mcs;
import com.mediatek.mcs.Utils.UIUtils;
import com.mediatek.mcs.domain.McsDataChannel;
import com.mediatek.mcs.domain.McsResponse;
import com.mediatek.mcs.domain.McsSession;
import com.mediatek.mcs.entity.DataChannelEntity;
import com.mediatek.mcs.entity.DataPointEntity;
import com.mediatek.mcs.entity.HistoryDataPointsEntity;
import com.mediatek.mcs.entity.api.DeviceInfoEntity;
import com.mediatek.mcs.entity.api.DeviceSummaryEntity;
import com.mediatek.mcs.net.McsJsonRequest;
import com.mediatek.mcs.net.RequestApi;
import com.mediatek.mcs.net.RequestManager;
import com.mediatek.mcs.socket.McsSocketListener;

import org.json.JSONObject;

import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {


    private Button confirm_device;
    private Button confirm_channel;
    private Button forward;
    private Button backward;
    private Button left;
    private Button right;
    private LinearLayout left_and_right;

    private DeviceInfoEntity mDeviceInfo;
    private McsDataChannel firstDataChannel;
    private DataPointEntity datapoint;
    private List<DataChannelEntity> dataChannels;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initView();
        Mcs.initialize(this, "62322442542559", "xxgtmDhOV6j7WXx6mCVgdJ69mbX0KYqQ");
        signIn();
    }

    public void confirmChannel(View view){
        dataChannels = mDeviceInfo.getDataChannels(); // a list of datachannelentity
        McsSocketListener socketListener = new McsSocketListener(
                new McsSocketListener.OnUpdateListener() {
                    @Override public void onUpdate(JSONObject response) {
                        // Socket message received
                    }
                }
        );
        firstDataChannel = new McsDataChannel(mDeviceInfo, dataChannels.get(7), socketListener);

        confirm_channel.setVisibility(View.GONE);
        forward.setVisibility(View.VISIBLE);
        backward.setVisibility(View.VISIBLE);
        left_and_right.setVisibility(View.VISIBLE);
//        left.setVisibility(View.VISIBLE);
//        right.setVisibility(View.VISIBLE);
//        System.out.println("data channel is " + dataChannels.get(7));
//        datapoint = dataChannels.get(7).getDataPoint();
//        System.out.println("datapoint is " + datapoint);
    }

    public void backward(View view){
        String data = "backward";
        firstDataChannel.submitDataPoint(new DataPointEntity.Values(data));
    }
    public void left(View view){
        String data = "left";
        firstDataChannel.submitDataPoint(new DataPointEntity.Values(data));
    }
    public void right(View view){
        String data = "right";
        firstDataChannel.submitDataPoint(new DataPointEntity.Values(data));
    }
    public void forward(View view){
        String data = "forward";
        firstDataChannel.submitDataPoint(new DataPointEntity.Values(data));
    }

    public void confirmDevice(View view){
        /**
         * GET device info.
         */
        String deviceId = "Dh0K5Kxe";

        McsJsonRequest request = new McsJsonRequest(
                RequestApi.DEVICE
                        .replace("{deviceId}", deviceId),
                new McsResponse.SuccessListener<JSONObject>() {
                    @Override public void onSuccess(JSONObject response) {
                        mDeviceInfo = UIUtils.getFormattedGson()
                                .fromJson(response.toString(), DeviceInfoEntity.class)
                                .getResults().get(0);

                        System.out.println("device info is " + mDeviceInfo);
                        confirm_device.setVisibility(View.GONE);
                        confirm_channel.setVisibility(View.VISIBLE);
                    }
                }
        );
        RequestManager.sendInBackground(request);
    }

    private void signIn(){
        // call in main thread
        String email = "milu0970488651.eed06@nctu.edu.tw";
        String pwd = "yyh@mcsMCS2020";
        McsSession.getInstance().requestSignIn(email, pwd,
                new McsResponse.SuccessListener<JSONObject>() {
                    @Override public void onSuccess(JSONObject response) {
                        // Signed in, back to UI thread
                        System.out.println("sign in success.");
                    }
                },
                /**
                 * Optional.
                 * Default error message shows in log.
                 */
                new McsResponse.ErrorListener() {
                    @Override public void onError(Exception e) {
                        // Sign in failed, back to UI thread
                    }
                }
        );
    }

    public void getDeviceList(View view){
        // Default method is GET
        int method = McsJsonRequest.Method.GET;
        String url = RequestApi.DEVICES;
        McsResponse.SuccessListener<JSONObject> successListener =
                new McsResponse.SuccessListener<JSONObject>() {
                    @Override public void onSuccess(JSONObject response) {
                        DeviceSummaryEntity[] summary = new Gson().fromJson(
                                response.toString(), DeviceSummaryEntity.class).getResults().toArray(new DeviceSummaryEntity[0]);

                        System.out.println(Arrays.toString(summary));
                    }
                };
        McsResponse.ErrorListener errorListener = new McsResponse.ErrorListener() {
            @Override public void onError(Exception e) {
                System.out.println("??????");
            }
        };
        McsJsonRequest request = new McsJsonRequest(method, url, successListener, errorListener);
        RequestManager.sendInBackground(request);
    }

    private void initView(){
        confirm_device = findViewById(R.id.confirm_device);
        confirm_channel = findViewById(R.id.confirm_channel);
        forward = findViewById(R.id.forward);
        backward = findViewById(R.id.backward);
        left = findViewById(R.id.left);
        right = findViewById(R.id.right);
        left_and_right = findViewById(R.id.left_and_right);
    }
}