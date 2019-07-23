package com.wearnotch.notchdemo;

import android.content.Context;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;

import java.util.Arrays;
import java.util.List;

public class FileReader {
    public List<ArrayList<String>>  readFile(Context context){
        try {

            List<ArrayList<String>> list = new ArrayList<ArrayList<String>>();
            //InputStream is = context.getAssets().open("data.txt");
            BufferedReader reader = new BufferedReader(new InputStreamReader(context.getAssets().open("data.txt")));

            String mLine;
            while((mLine = reader.readLine()) != null) {
                list.add(toArrayList(mLine));
            }
            return list;

        } catch (IOException e) {
            e.printStackTrace();
        }
        return  null;
    }
    private ArrayList<String> toArrayList(String s) {
        String[] commaSeparatedArr = s.split("\\s*,\\s*");
        ArrayList<String> result = new ArrayList<String>(Arrays.asList(commaSeparatedArr));

        return result;
    }
}
